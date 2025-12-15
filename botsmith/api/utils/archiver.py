import shutil
import io
import os
from pathlib import Path

def zip_project(project_path: Path) -> io.BytesIO:
    """
    Zips a directory in-memory and returns the bytes.
    """
    memory_file = io.BytesIO()
    
    # shutil.make_archive expects a file path, so we use a temp dir approach 
    # OR we use zipfile directly for in-memory
    import zipfile
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = Path(root) / file
                archive_name = file_path.relative_to(project_path)
                zf.write(file_path, archive_name)
    
    memory_file.seek(0)
    return memory_file
