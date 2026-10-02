from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import token_user_id
from app.models.entities import Membership, Project, User

oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def current_user(token: str = Depends(oauth), db: Session = Depends(get_db)) -> User:
    user_id = token_user_id(token)
    user = db.get(User, user_id) if user_id else None
    if not user:
        raise HTTPException(401, "Invalid or expired access token")
    return user


def project_access(project_id: int, user: User, db: Session) -> tuple[Project, Membership]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    membership = db.query(Membership).filter_by(
        organization_id=project.organization_id, user_id=user.id
    ).first()
    if not membership:
        raise HTTPException(404, "Project not found")
    return project, membership
