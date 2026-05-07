import os


def check_file_exists(file_path: str) -> bool:
    """Check if a file exists at the given path."""
    try:
        os.stat(file_path)
        return True
    except OSError:
        return False
