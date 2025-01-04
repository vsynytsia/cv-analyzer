from typing import Annotated

import httpx
import jinja2
from fastapi import Depends, HTTPException, status
from google import generativeai as genai

from app.core.config import settings


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


async def get_httpx_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client


HttpxClientDep = Annotated[httpx.AsyncClient, Depends(get_httpx_client)]


async def get_jinja_environment() -> jinja2.Environment:
    loader = jinja2.FileSystemLoader(settings.PROMPTS_DIR)
    return jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)


JinjaEnvDep = Annotated[jinja2.Environment, Depends(get_jinja_environment)]
