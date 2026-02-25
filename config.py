import os
import shutil
import random
import string
from pathlib import Path
from typing import Union

# Base directories
BASE_DIR = Path(__file__).resolve().parent
SANDBOX_DIR = BASE_DIR / "sandbox"
LOG_DIR = BASE_DIR / "logs"

def setup_sandbox():
    """
    Initializes the sandbox and log directories.
    Clears the sandbox if it already exists to start fresh.
    """
    if SANDBOX_DIR.exists():
        shutil.rmtree(SANDBOX_DIR)
    
    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[*] Sandbox initialized at: {SANDBOX_DIR}")
    print(f"[*] Logs initialized at: {LOG_DIR}")

def is_safe_path(path_to_check: Union[str, Path]) -> bool:
    """
    Ensures that a given path resolves to inside the SANDBOX_DIR.
    Prevents directory traversal attacks (e.g., ../../etc/passwd)
    """
    try:
        # Resolve to gets the absolute path and normalizes . and ..
        resolved_path = Path(path_to_check).resolve()
        # Check if SANDBOX_DIR is a parent of the resolved path
        return SANDBOX_DIR in resolved_path.parents or resolved_path == SANDBOX_DIR
    except Exception:
        return False

def safe_open(file_path: Union[str, Path], mode: str = 'r'):
    """
    Wrapper around open() that enforces is_safe_path.
    Raises ValueError if the path is outside the sandbox.
    """
    if not is_safe_path(file_path):
        raise ValueError(f"Path operation denied (outside sandbox): {file_path}")
    return open(file_path, mode)

def safe_unlink(file_path: Union[str, Path]):
    """
    Wrapper around Path.unlink() or os.unlink() that enforces is_safe_path.
    Raises ValueError if the path is outside the sandbox.
    """
    if not is_safe_path(file_path):
        raise ValueError(f"Delete operation denied (outside sandbox): {file_path}")
    Path(file_path).unlink(missing_ok=True)

def safe_walk(directory_path: Union[str, Path] = SANDBOX_DIR):
    """
    Wrapper around os.walk that only visits directories inside the sandbox.
    Defaults to walking the entire sandbox.
    """
    if not is_safe_path(directory_path):
        raise ValueError(f"Walk operation denied (outside sandbox): {directory_path}")
        
    for root, dirs, files in os.walk(directory_path):
        # Double-check every yielded root just to be paranoid
        if not is_safe_path(root):
            continue
        yield root, dirs, files


def generate_dummy_files(num_files: int = 20, max_depth: int = 3, max_size_kb: int = 50):
    """
    Populates the sandbox with dummy files and folders for testing.
    """
    print(f"[*] Generating {num_files} dummy files in sandbox...")
    
    extensions = [".txt", ".log", ".csv", ".dat"]
    current_files = 0
    
    # Create some nested folders
    dirs_to_use = [SANDBOX_DIR]
    for _ in range(max_depth):
        new_dir = random.choice(dirs_to_use) / ''.join(random.choices(string.ascii_lowercase, k=8))
        new_dir.mkdir(exist_ok=True)
        dirs_to_use.append(new_dir)

    while current_files < num_files:
        target_dir = random.choice(dirs_to_use)
        ext = random.choice(extensions)
        filename = f"dummy_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}{ext}"
        filepath = target_dir / filename
        
        try:
            with safe_open(filepath, 'w') as f:
                # Write random data up to max_size_kb
                size = random.randint(1, max_size_kb * 1024)
                data = ''.join(random.choices(string.ascii_letters + string.digits, k=min(size, 1024)))
                f.write(data)
                
            current_files += 1
        except Exception as e:
            print(f"[!] Error creating dummy file {filepath}: {e}")
            
    print(f"[*] Successfully created {current_files} dummy files.")

if __name__ == "__main__":
    setup_sandbox()
    generate_dummy_files()
