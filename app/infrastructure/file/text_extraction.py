import pymupdf

from app.core.exceptions import FileTextExtractionError
from app.core.interfaces import IFileTextExtractor

__all__ = ["PdfTextExtractorI", "FileTextExtractorFactory"]


class PdfTextExtractorI(IFileTextExtractor):
    def extract_text(self, file: bytes) -> str:
        try:
            with pymupdf.open(stream=file, filetype="pdf") as doc:
                pages = [page.get_text().strip() for page in doc]
                return " ".join(pages)
        except Exception as ex:
            raise FileTextExtractionError() from ex


class FileTextExtractorFactory:
    @staticmethod
    def from_file_extension(file_extension: str) -> "IFileTextExtractor":
        mapping = {"pdf": PdfTextExtractorI}
        if (file_text_extractor := mapping.get(file_extension)) is None:
            raise NotImplementedError(f"File text extractor for '{file_extension}' files is not implemented")

        return file_text_extractor()
