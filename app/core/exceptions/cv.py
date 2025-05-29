from .base import BusinessError

__all__ = ["UnsupportedCVLanguage"]


class UnsupportedCVLanguage(BusinessError):
    def __init__(self, language: str) -> None:
        self.language = language
        super().__init__(f"CV has unsupported language: {language}")
