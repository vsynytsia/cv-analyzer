from pydantic import BaseModel

__all__ = ["File"]


class File(BaseModel):
    content: bytes
    filename: str
    size: int

    @property
    def extension(self) -> str | None:
        try:
            return self.filename.split(".")[-1].lower()
        except Exception:
            return None
