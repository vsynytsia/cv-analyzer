import abc

import jinja2

__all__ = ["PromptManager", "JinjaPromptManager"]


class PromptManager(abc.ABC):
    @abc.abstractmethod
    def render_prompt_template(self, prompt_template_path: str, **prompt_params) -> str:
        raise NotImplementedError


class JinjaPromptManager(PromptManager):
    def __init__(self) -> None:
        self._jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("app/prompts"), trim_blocks=True, lstrip_blocks=True
        )

    def render_prompt_template(self, prompt_template_path: str, **prompt_params) -> str:
        prompt_template = self._jinja_env.get_template(prompt_template_path)
        return prompt_template.render(**prompt_params)
