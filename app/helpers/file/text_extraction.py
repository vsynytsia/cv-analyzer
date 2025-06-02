import pymupdf

from app.core.exceptions import FileTextExtractionError
from app.core.interfaces import FileTextExtractor

__all__ = ["PdfTextExtractor", "FileTextExtractorFactory"]


class PdfTextExtractor(FileTextExtractor):
    def extract_text(self, file: bytes) -> str:
        try:
            with pymupdf.open(stream=file, filetype="pdf") as doc:
                pages = [page.get_text().strip() for page in doc]
                return " ".join(pages)
        except Exception as ex:
            raise FileTextExtractionError() from ex


class FileTextExtractorFactory:
    @staticmethod
    def from_file_extension(file_extension: str) -> "FileTextExtractor":
        mapping = {"pdf": PdfTextExtractor}
        if (file_text_extractor := mapping.get(file_extension)) is None:
            raise NotImplementedError(f"File text extractor for '{file_extension}' files is not implemented")

        return file_text_extractor()
