from fake_useragent import UserAgent
from httpx import AsyncClient, Response


async def make_async_http_get_request_with_random_user_agent(
    client: AsyncClient, url: str, params: dict | None = None
) -> Response:
    headers = create_http_headers_with_random_user_agent()
    return await make_async_http_get_request(client, url, headers, params)


async def make_async_http_get_request(
    client: AsyncClient, url: str, headers: dict | None = None, params: dict | None = None
) -> Response:
    response = await client.get(url, headers=headers, params=params)
    return response.raise_for_status()


def create_http_headers_with_random_user_agent() -> dict[str, str]:
    user_agent = make_random_user_agent()
    return create_http_headers_with_user_agent(user_agent)


def create_http_headers_with_user_agent(user_agent: str) -> dict[str, str]:
    return {"User-Agent": user_agent}


def make_random_user_agent() -> str:
    return UserAgent().random
