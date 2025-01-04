import pymupdf
from fastapi import UploadFile

from app.core.config import settings


async def extract_text_from_pdf(pdf: UploadFile) -> str:
    file_content_bytes = await pdf.read()

    with pymupdf.open(stream=file_content_bytes, filetype="pdf") as doc:
        text = " ".join([page.get_text().strip() for page in doc])

    return text[: settings.MAX_UPLOAD_FILE_SIZE_CHARACTERS]


def is_pdf(file: UploadFile) -> bool:
    return file_has_extension(file, ".pdf")


def file_has_extension(file: UploadFile, extension: str) -> bool:
    return file.filename.endswith(extension)


def file_size_exceeds_limit(file: UploadFile) -> bool:
    return file.size > settings.MAX_UPLOAD_FILE_SIZE_BYTES
