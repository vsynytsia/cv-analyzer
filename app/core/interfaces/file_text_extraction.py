from typing import Protocol

from app.models.domain import File

__all__ = ["IFileTextExtractor"]


class IFileTextExtractor(Protocol):
    def extract_text(self, file: File) -> str:
        pass
