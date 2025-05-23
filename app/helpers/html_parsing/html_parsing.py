from bs4 import BeautifulSoup

__all__ = ["HtmlParser"]


class HtmlParser:
    def __init__(self, html_content: bytes) -> None:
        self._soup = BeautifulSoup(html_content, "html.parser")

    def find_all(self, *args, **kwargs):
        return self._soup.find_all(*args, **kwargs)

    def extract_first_line_of_multiline_string_safe(self, selector: str, **kwargs) -> str | None:
        try:
            return self._soup.find(selector, **kwargs).text.strip().splitlines()[0]
        except Exception:
            return None

    def extract_element_text_safe(self, selector: str, separator: str = "", **kwargs) -> str | None:
        try:
            return self.extract_element_text_unsafe(selector, separator, **kwargs)
        except Exception:
            return None

    def extract_element_text_unsafe(self, selector: str, separator: str = "", **kwargs) -> str:
        return self._soup.find(selector, **kwargs).get_text(separator=separator, strip=True)
