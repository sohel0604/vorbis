import io
import re
import stat
import zipfile
from pathlib import PurePosixPath

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import Base, engine, get_db
from app.core.deps import current_user, project_access
from app.core.security import hash_password, issue_token, verify_password
from app.models.entities import Membership, Organization, Project, SourceFile, Symbol, User
from app.schemas.api import LoginInput, ProjectInput, RegisterInput
from app.services.indexer import SKIP_DIRS, classify, language_for, symbols_for
from app.services.learning import curriculum, grounded_answer

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vorbis API", version="0.1.0", description="Evidence-grounded software onboarding platform")
app.add_middleware(CORSMiddleware, allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "vorbis-api"}


@app.post("/api/v1/auth/register", status_code=201)
def register(payload: RegisterInput, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(409, "An account with this email already exists")
    user = User(email=email, name=payload.name, password_hash=hash_password(payload.password))
    org = Organization(name=payload.organization_name)
    db.add_all([user, org]); db.flush()
    db.add(Membership(user_id=user.id, organization_id=org.id, role="owner")); db.commit()
    return {"access_token": issue_token(user.id), "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}, "organization": {"id": org.id, "name": org.name}}


@app.post("/api/v1/auth/login")
def login(payload: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Email or password is incorrect")
    return {"access_token": issue_token(user.id), "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}


@app.get("/api/v1/me")
def me(user: User = Depends(current_user), db: Session = Depends(get_db)):
    memberships = db.query(Membership).filter_by(user_id=user.id).all()
    return {"id": user.id, "email": user.email, "name": user.name, "organizations": [{"id": m.organization_id, "name": m.organization.name, "role": m.role} for m in memberships]}


@app.get("/api/v1/projects")
def list_projects(user: User = Depends(current_user), db: Session = Depends(get_db)):
    org_ids = [m.organization_id for m in db.query(Membership).filter_by(user_id=user.id).all()]
    return [{"id": p.id, "organization_id": p.organization_id, "name": p.name, "status": p.status, "source_type": p.source_type, "file_count": len(p.files)} for p in db.query(Project).filter(Project.organization_id.in_(org_ids)).all()] if org_ids else []


@app.post("/api/v1/projects", status_code=201)
def create_project(payload: ProjectInput, organization_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    membership = db.query(Membership).filter_by(user_id=user.id, organization_id=organization_id).first()
    if not membership: raise HTTPException(404, "Organization not found")
    project = Project(organization_id=organization_id, name=payload.name.strip())
    db.add(project); db.commit(); db.refresh(project)
    return {"id": project.id, "name": project.name, "status": project.status}


@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    return {"id": project.id, "name": project.name, "status": project.status, "source_type": project.source_type, "file_count": len(project.files), "symbol_count": len(project.symbols)}


@app.post("/api/v1/projects/{project_id}/upload", status_code=202)
async def upload_zip(project_id: int, archive: UploadFile = File(...), user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, membership = project_access(project_id, user, db)
    if membership.role == "viewer": raise HTTPException(403, "Viewer role cannot upload source")
    if not archive.filename or not archive.filename.lower().endswith(".zip"): raise HTTPException(415, "Upload a .zip archive")
    limit = settings.max_upload_mb * 1024 * 1024
    data = await archive.read(limit + 1)
    if len(data) > limit: raise HTTPException(413, f"Archive exceeds {settings.max_upload_mb} MB limit")
    try: zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile: raise HTTPException(400, "Invalid ZIP archive") from None
    safe_entries = []
    seen_paths = set()
    total_uncompressed = 0
    if len(zf.infolist()) > 20000: raise HTTPException(413, "Archive contains too many entries")
    for info in zf.infolist():
        path = PurePosixPath(info.filename)
        mode = info.external_attr >> 16
        if path.is_absolute() or ".." in path.parts or "\\" in info.filename or stat.S_ISLNK(mode):
            raise HTTPException(400, "Archive contains an unsafe path or symbolic link")
        if not path.parts or any(part in SKIP_DIRS for part in path.parts): continue
        if info.is_dir(): continue
        if info.flag_bits & 0x1: raise HTTPException(400, "Encrypted ZIP entries are not supported")
        normalized_path = path.as_posix()
        if normalized_path in seen_paths: raise HTTPException(400, "Archive contains duplicate file paths")
        seen_paths.add(normalized_path)
        total_uncompressed += info.file_size
        if info.file_size > 5 * 1024 * 1024 or total_uncompressed > limit * 5:
            raise HTTPException(413, "Archive expands beyond the permitted indexing size")
        if info.compress_size and info.file_size / info.compress_size > 200:
            raise HTTPException(400, "Archive has an unsafe compression ratio")
        safe_entries.append((info, normalized_path))
    # Replace the previous index only after archive validation succeeded.
    db.query(Symbol).filter_by(project_id=project.id).delete()
    db.query(SourceFile).filter_by(project_id=project.id).delete()
    indexed = 0
    for info, path in safe_entries:
        if len(path) > 1024: continue
        try: raw = zf.read(info)
        except (zipfile.BadZipFile, RuntimeError): raise HTTPException(400, "Archive contains a corrupt or unreadable entry") from None
        content = None
        if b"\x00" not in raw[:8192]:
            try: content = raw[:1024 * 1024].decode("utf-8")
            except UnicodeDecodeError: pass
        lang = language_for(path)
        source = SourceFile(project_id=project.id, path=path, language=lang, size_bytes=info.file_size, content=content)
        db.add(source); db.flush()
        if content and lang != "unknown":
            for symbol in symbols_for(path, content):
                db.add(Symbol(project_id=project.id, file_id=source.id, name=symbol["name"], kind=symbol["kind"], start_line=symbol["start"], end_line=symbol["end"]))
        indexed += 1
    project.status = "indexed"; db.commit()
    return {"project_id": project.id, "status": "indexed", "files_indexed": indexed, "symbols_indexed": db.query(Symbol).filter_by(project_id=project.id).count()}


@app.get("/api/v1/projects/{project_id}/files")
def files(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    return [{"path": f.path, "language": f.language, "size_bytes": f.size_bytes, "component": classify(f.path)} for f in project.files]


@app.get("/api/v1/projects/{project_id}/symbols")
def symbols(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    return [{"path": s.file.path, "name": s.name, "kind": s.kind, "start_line": s.start_line, "end_line": s.end_line} for s in project.symbols]


@app.get("/api/v1/projects/{project_id}/architecture")
def architecture(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    grouped = {}
    for f in project.files: grouped.setdefault(classify(f.path), []).append(f.path)
    nodes = list(grouped)
    lines = ["flowchart LR"]
    for node in nodes: lines.append(f'  {re.sub("[^A-Za-z0-9_]", "_", node)}["{node.title()} ({len(grouped[node])} files)"]')
    return {"mermaid": "\n".join(lines), "components": grouped, "note": "This is a file grouping only. Import, call, and runtime relationships are not resolved."}


@app.get("/api/v1/projects/{project_id}/curriculum")
def get_curriculum(project_id: int, role: str = "full stack", user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    return curriculum(project.name, role, [f.path for f in project.files])


@app.post("/api/v1/projects/{project_id}/mentor")
def mentor(project_id: int, payload: dict, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    question = str(payload.get("question", "")).strip()
    if not question or len(question) > 2000: raise HTTPException(422, "Question must be 1–2000 characters")
    evidence = [{"path": f.path, "content": f.content} for f in project.files if f.content]
    return grounded_answer(question, evidence)


@app.get("/api/v1/projects/{project_id}/readiness")
def readiness(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project, _ = project_access(project_id, user, db)
    count = len(project.files)
    return {"project_id": project_id, "signals": {"architecture": None, "code_index": min(100, len(project.symbols) * 2), "hands_on": 0, "security": 0}, "status": "baseline" if count else "awaiting-source", "note": "Readiness is an onboarding progress scaffold and requires learner activity to become meaningful."}
