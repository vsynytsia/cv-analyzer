import jinja2

from app.core.exceptions import PromptTemplateNotFound
from app.core.interfaces import IPromptManager

__all__ = ["JinjaIPromptManager"]


class JinjaIPromptManager(IPromptManager):
    def __init__(self) -> None:
        self._jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("app/prompts"), trim_blocks=True, lstrip_blocks=True
        )

    def render_prompt_template(self, prompt_template_path: str, **prompt_params) -> str:
        prompt_template = self.get_prompt_template(prompt_template_path)
        return prompt_template.render(**prompt_params)

    def get_prompt_template(self, prompt_template_path: str) -> jinja2.Template:
        try:
            return self._jinja_env.get_template(prompt_template_path)
        except jinja2.TemplateNotFound as ex:
            raise PromptTemplateNotFound(prompt_template_path) from ex
