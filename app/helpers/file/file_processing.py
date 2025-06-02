import logging

from app.core.exceptions import FileMalformed, FileTooLarge, UnsupportedFileType
from app.models.domain import File

from .text_extraction import FileTextExtractorFactory

__all__ = ["FileProcessor"]


class FileProcessor:
    SUPPORTED_FILE_TYPES = ("pdf",)

    def __init__(self, max_file_size_bytes: int) -> None:
        self.max_file_size_bytes = max_file_size_bytes
        self._logger = logging.getLogger(self.__class__.__name__)

    async def extract_text(self, file: File) -> str:
        self.validate(file)

        file_text_extractor = FileTextExtractorFactory.from_file_extension(file.extension)
        text = file_text_extractor.extract_text(file.content)
        self._logger.info("Extracted text from file %s", file.filename)

        return text

    def validate(self, file: File) -> None:
        if file.content is None or file.size is None or file.filename is None:
            raise FileMalformed()

        if file.extension is None:
            raise UnsupportedFileType(file.filename, self.SUPPORTED_FILE_TYPES)

        if file.size > self.max_file_size_bytes:
            raise FileTooLarge(file.size, self.max_file_size_bytes)
