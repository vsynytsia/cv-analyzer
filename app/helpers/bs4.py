from bs4 import BeautifulSoup


def extract_first_line_of_multiline_string_safe(soup: BeautifulSoup, selector: str, **kwargs) -> str | None:
    try:
        return soup.find(selector, **kwargs).text.strip().splitlines()[0]
    except Exception:
        return None


def extract_element_text_safe(soup: BeautifulSoup, selector: str, separator: str = "", **kwargs) -> str | None:
    try:
        return extract_element_text_unsafe(soup, selector, separator, **kwargs)
    except Exception:
        return None


def extract_element_text_unsafe(soup: BeautifulSoup, selector: str, separator: str = "", **kwargs) -> str:
    return soup.find(selector, **kwargs).get_text(separator=separator, strip=True)


def get_bs4_html_parser(html_content: bytes) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")
