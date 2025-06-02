from typing import Iterable

from .base import UserInputError

__all__ = [
    "UnsupportedFileType",
    "FileTextExtractionError",
    "FileTooLarge",
    "FileMalformed",
]


class UnsupportedFileType(UserInputError):
    code = "unsupported_file_type"

    def __init__(self, filename: str, supported_types: Iterable[str]) -> None:
        self.filename = filename
        self.supported_types = supported_types
        super().__init__(f"File '{filename}' has unsupported type. Supported types: {supported_types}")


class FileTextExtractionError(UserInputError):
    code = "file_text_extraction_error"

    def __init__(self) -> None:
        super().__init__("Failed to extract text from file")


class FileTooLarge(UserInputError):
    code = "file_too_large"

    def __init__(self, size: int, max_size: int) -> None:
        self.size = size
        self.max_size = max_size
        super().__init__(f"File has size {size}, which exceeds maximum size: {max_size} ")


class FileMalformed(UserInputError):
    code = "file_malformed"

    def __init__(self) -> None:
        super().__init__("File is malformed")
