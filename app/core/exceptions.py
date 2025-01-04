class UnsupportedLanguageError(Exception):
    def __init__(self, language: str) -> None:
        self.language = language
        message = f'Encountered unsupported text language: "{self.language}".'
        super().__init__(message)


class GeminiAPIError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TranslationAPIError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
