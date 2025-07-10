from pathlib import Path


class FileUtils:
    """Utility class for file operations.

    Provides static methods to read files using absolute or relative paths.
    """

    @staticmethod
    def read_file_absolute(path: str) -> str:
        return Path(path).read_text(encoding='utf-8')

    @staticmethod
    def read_file_relative(current_path: str, relative_path: str) -> str:
        dir_path = Path(current_path).parent
        file_path = dir_path / relative_path
        return Path(file_path).read_text(encoding='utf-8')
