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

    def mkdir(self, path: str):
        full_path = self.root / path
        full_path.mkdir(parents=True, exist_ok=True)

    def write_file(self, path: str, content: str):
        full_path = self.root / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
