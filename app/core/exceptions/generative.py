from typing import Type

from pydantic import BaseModel

from .base import ExternalServiceError, InternalError

__all__ = ["PromptTemplateNotFound", "ContentGenerationError", "GenerativeResponseModelConversionError"]


class PromptTemplateNotFound(InternalError):
    code = "prompt_template_not_found"

    def __init__(self, prompt_template_path: str) -> None:
        self.prompt_template_path = prompt_template_path
        super().__init__(f"Prompt template '{prompt_template_path}' is not found.")


class ContentGenerationError(ExternalServiceError):
    code = "content_generation_error"

    def __init__(self, prompt: str) -> None:
        super().__init__(f"Failed to generate content for prompt: {prompt}")


class GenerativeResponseModelConversionError(ExternalServiceError):
    code = "generative_response_model_conversion_error"

    def __init__(self, generative_response: str, model: Type[BaseModel]) -> None:
        self.generative_response = generative_response
        self.model = model
        super().__init__(f"Failed to convert generative response {generative_response} to pydantic model {model}")
