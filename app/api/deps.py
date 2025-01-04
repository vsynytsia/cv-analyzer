from typing import Annotated, Any, AsyncGenerator

import jinja2
from fastapi import Depends, HTTPException, status
from google import generativeai as genai

from app.core.config import settings
from app.helpers.http import AsyncHTTPClient


async def get_genai_client() -> genai.GenerativeModel:
    api_key = settings.GOOGLE_GENAI_API_KEY
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="google-generativeai API key is not configured",
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-002")


GeminiClientDep = Annotated[genai.GenerativeModel, Depends(get_genai_client)]


async def get_http_client() -> AsyncGenerator[AsyncHTTPClient, Any]:
    async with AsyncHTTPClient() as client:
        yield client


HttpClientDep = Annotated[AsyncHTTPClient, Depends(get_http_client)]


async def get_jinja_environment() -> jinja2.Environment:
    loader = jinja2.FileSystemLoader("app/services/")
    return jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)


JinjaEnvDep = Annotated[jinja2.Environment, Depends(get_jinja_environment)]
