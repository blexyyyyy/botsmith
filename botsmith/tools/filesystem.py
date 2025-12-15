from pathlib import Path


class FileSystemTool:
    """
    Safe filesystem operations scoped to a base directory.
    """

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _resolve(self, relative_path: str) -> Path:
        path = (self.base_dir / relative_path).resolve()
        if not str(path).startswith(str(self.base_dir)):
            raise ValueError("Path traversal detected")
        return path

    def mkdir(self, relative_path: str):
        path = self._resolve(relative_path)
        path.mkdir(parents=True, exist_ok=True)

    def write_file(self, relative_path: str, content: str):
        path = self._resolve(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def exists(self, relative_path: str) -> bool:
        return self._resolve(relative_path).exists()
