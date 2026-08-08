
import sys
from pathlib import Path

def add_path(path:str)->None:
    """
    Add a directory to the Python module search path.

    The provided path is expanded, resolved to an absolute path, and added
    to ``sys.path`` if it is not already present. The path is inserted at
    the beginning of ``sys.path`` so that modules in this directory have
    priority during imports.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the directory containing the Python modules to import.

    Raises
    ------
    FileNotFoundError
        If the specified path does not exist.
    NotADirectoryError
        If the specified path exists but is not a directory.
    """
    path = Path(path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    path_str = str(path)

    if path_str not in sys.path:
        sys.path.insert(0, path_str)

# add_path('../scripts/')
