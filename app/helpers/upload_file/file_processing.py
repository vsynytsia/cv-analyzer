import functools
import logging

from fastapi import UploadFile

from app.core.exceptions import FileMalformed, FileTooLarge, UnsupportedFileType

from .text_extraction import FileTextExtractorFactory

__all__ = ["UploadFileProcessor"]


class UploadFileProcessor:
    SUPPORTED_FILE_TYPES = ("pdf",)

    def __init__(self, upload_file: UploadFile, max_file_size_bytes: int) -> None:
        self.upload_file = upload_file
        self.max_file_size_bytes = max_file_size_bytes
        self._logger = logging.getLogger(self.__class__.__name__)

    async def extract_text(self) -> str:
        self._validate()

        file_content_bytes = await self.upload_file.read()

        file_text_extractor = FileTextExtractorFactory.from_file_extension(self.extension)
        text = file_text_extractor.extract_text(file_content_bytes)
        self._logger.info("Extracted text from file %s", self.filename)

        return text

    @functools.cached_property
    def filename(self) -> str | None:
        return self.upload_file.filename

    @functools.cached_property
    def size_bytes(self) -> int | None:
        return self.upload_file.size

    @functools.cached_property
    def extension(self) -> str:
        try:
            return self.filename.split(".")[-1]
        except Exception as ex:
            raise UnsupportedFileType(self.filename, self.SUPPORTED_FILE_TYPES) from ex

    def _validate(self) -> None:
        if self.size_bytes is None or self.filename is None:
            raise FileMalformed()

        if self.size_bytes > self.max_file_size_bytes:
            raise FileTooLarge(self.size_bytes, self.max_file_size_bytes)
