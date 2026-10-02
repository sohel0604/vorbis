import ast
import re

EXTENSIONS = {
    ".py": "python", ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript",
    ".cjs": "javascript", ".ts": "typescript", ".tsx": "typescript", ".java": "java",
    ".go": "go", ".cs": "csharp", ".sql": "sql", ".md": "markdown",
    ".yaml": "yaml", ".yml": "yaml", ".json": "json", ".toml": "toml",
}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "target", ".venv", "venv", "vendor", "__pycache__"}
SYMBOL_RE = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?(?:class|function|interface|type|enum|def)\s+([\w$]+)")


def language_for(path: str) -> str:
    from pathlib import PurePosixPath
    return EXTENSIONS.get(PurePosixPath(path).suffix.lower(), "unknown")


def symbols_for(path: str, content: str) -> list[dict]:
    lang = language_for(path)
    if lang == "python":
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []
        result = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                result.append({"name": node.name, "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                               "start": node.lineno, "end": getattr(node, "end_lineno", node.lineno)})
        return result
    result = []
    for n, line in enumerate(content.splitlines(), 1):
        match = SYMBOL_RE.match(line)
        if match:
            kind = re.search(r"\b(class|function|interface|type|enum|def)\b", line)
            result.append({"name": match.group(1), "kind": kind.group(1) if kind else "symbol", "start": n, "end": n})
    return result


def classify(path: str) -> str:
    p = path.lower()
    if any(x in p for x in ("frontend", "client", "web", "ui")): return "frontend"
    if any(x in p for x in ("test", "spec")): return "tests"
    if any(x in p for x in ("migration", "schema", "model", "entity")): return "data"
    if any(x in p for x in ("api", "route", "controller")): return "api"
    if any(x in p for x in ("service", "worker", "job")): return "service"
    return "source"
