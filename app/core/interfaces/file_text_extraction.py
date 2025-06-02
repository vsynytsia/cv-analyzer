import abc

__all__ = ["FileTextExtractor"]


class FileTextExtractor(abc.ABC):
    @abc.abstractmethod
    def extract_text(self, file: bytes) -> str:
        raise NotImplementedError
