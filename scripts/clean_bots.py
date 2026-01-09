import shutil
import os
from pathlib import Path

def clean_directory(dir_path):
    path = Path(dir_path)
    if not path.exists():
        print(f"Directory not found: {dir_path}")
        return

    print(f"Cleaning {dir_path}...")
    for item in path.iterdir():
        if item.name == ".gitkeep":
            continue
            
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            print(f"  Deleted: {item.name}")
        except Exception as e:
            print(f"  Failed to delete {item.name}: {e}")

def main():
    root = Path(__file__).parent.parent
    
    # Clean 'generated'
    clean_directory(root / "generated")
    
    # Clean 'workspace' (legacy output)
    clean_directory(root / "workspace")

    # Clean 'generated_bots' (current output)
    clean_directory(root / "generated_bots")
    
    print("\nCleanup complete!")

if __name__ == "__main__":
    main()
