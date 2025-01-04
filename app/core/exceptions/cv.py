from .base import BusinessException

__all__ = ["UnsupportedCVLanguage"]


class UnsupportedCVLanguage(BusinessException):
    def __init__(self, language: str) -> None:
        self.language = language
        super().__init__(f"CV has unsupported language: {language}")
