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

    Example
    ------
    add_path('../scripts/')
    """
    path = Path(path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    path_str = str(path)

    if path_str not in sys.path:
        sys.path.insert(0, path_str)

def get_files_by_extension(path: str | Path, extension: str) -> list[Path]:
    """
    Find all files con una extension recursively inside a directory.

    Parameters
    ----------
    path : str or pathlib.Path
        Directory in which to search for files.
    extension: str
        Extensión de los archivos a buscar

    Returns
    -------
    list of pathlib.Path
        List of paths to the files found recursively.

    Raises
    ------
    FileNotFoundError
        If the specified directory does not exist.
    NotADirectoryError
        If the specified path is not a directory.
    PermissionError
        If the directory cannot be accessed due to insufficient permissions.

    Examples
    --------
    >>> get_files_by_extension("data", "csv")
    [PosixPath('data/file1.csv'), PosixPath('data/subdir/file2.csv')]
    """
    directory = Path(path)

    if not directory.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {path}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {path}"
        )
    try:
        return list(directory.rglob(f"*.{extension}"))
    except PermissionError as exc:
        raise PermissionError(
            f"Permission denied while accessing directory: {path}"
        ) from exc
