from typing import Protocol

__all__ = ["IFileTextExtractor"]


class IFileTextExtractor(Protocol):
    def extract_text(self, file: bytes) -> str:
        pass
