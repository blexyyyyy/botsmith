import os
from pathlib import Path

class LocalFileSystem:
    """
    Simple filesystem abstraction for agents.
    All paths are relative to a root (defaults to generated/).
    """
    def __init__(self, root_path: str = "generated"):
        self.root = Path(root_path)
        self.root.mkdir(parents=True, exist_ok=True)

    def _sanitize_path(self, path: str) -> Path:
        # Split path and strip each component to prevent trailing space issues on Windows
        parts = [p.strip() for p in Path(path).parts]
        return self.root.joinpath(*parts)

    def mkdir(self, path: str):
        full_path = self._sanitize_path(path)
        full_path.mkdir(parents=True, exist_ok=True)

    def write_file(self, path: str, content: str):
        full_path = self._sanitize_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
