from collections import Counter


def curriculum(project_name: str, role: str, files: list[str]) -> dict:
    counts = Counter()
    for path in files:
        lower = path.lower()
        if any(x in lower for x in ("test", "spec")): counts["Testing"] += 1
        elif any(x in lower for x in ("api", "route", "controller")): counts["API"] += 1
        elif any(x in lower for x in ("model", "schema", "migration")): counts["Data"] += 1
        elif any(x in lower for x in ("frontend", "client", "ui")): counts["UI"] += 1
        else: counts["Core"] += 1
    focus = {"backend": ["API", "Core", "Data", "Testing"], "frontend": ["UI", "API", "Testing"],
             "devops": ["Core", "Testing", "API"], "qa": ["Testing", "API", "Core"],
             "tech lead": ["Core", "API", "Data", "Testing"]}.get(role.lower(), ["Core", "API", "Data", "Testing"])
    return {"project": project_name, "role": role, "days": [
        {"day": 1, "title": "Orient and map the system", "milestones": ["Read the project overview", "Trace the main entry points"], "evidence": list(files[:8])},
        {"day": 2, "title": "Follow a feature end to end", "milestones": [f"Explore {area.lower()} code" for area in focus[:3]], "evidence": [p for p in files if any(x.lower() in p.lower() for x in focus)][:10]},
        {"day": 3, "title": "Make a safe first contribution", "milestones": ["Run the existing checks", "Choose a scoped starter task", "Review the change with a maintainer"], "evidence": [p for p in files if "test" in p.lower()][:8]},
    ], "inventory": dict(counts)}


def grounded_answer(question: str, evidence: list[dict]) -> dict:
    if not evidence:
        return {"answer": "I could not find indexed source evidence for this project yet. Upload and index source files first.", "citations": [], "grounded": False}
    terms = [w.lower() for w in question.split() if len(w) > 3]
    if not terms:
        return {"answer": "Please include a code or feature name so I can find matching repository evidence.", "citations": [], "grounded": False}
    ranked = sorted(evidence, key=lambda x: sum(t in (x.get("path", "") + " " + (x.get("content") or "")).lower() for t in terms), reverse=True)
    picks = [item for item in ranked if any(term in (item.get("path", "") + " " + (item.get("content") or "")).lower() for term in terms)][:3]
    if not picks:
        return {"answer": "I could not find matching indexed source evidence for that question. Try a symbol, file, or feature name from this repository.", "citations": [], "grounded": False}
    citations = []
    for item in picks:
        lines = (item.get("content") or "").splitlines()
        line_number = next((i for i, line in enumerate(lines, 1) if any(term in line.lower() for term in terms)), 1)
        excerpt = "\n".join(f"{i}: {line}" for i, line in enumerate(lines[max(0, line_number - 2):line_number + 1], max(1, line_number - 1)))
        citations.append({"path": item["path"], "line": line_number, "excerpt": excerpt})
    return {"answer": "Based on the indexed repository, these files are the closest evidence for your question. Follow the cited entry points and symbols to trace the behavior; the local mentor only states claims supported by indexed source excerpts.", "citations": citations, "grounded": bool(citations)}
