from jinja2 import Environment
from src.services.render_template_service.abc import AbstractRenderTemplateService


class RenderTemplateService(AbstractRenderTemplateService):
    def __init__(self, env: Environment):
        self._env = env

    async def render_template(self, value: str, template: str):

        template = self._env.get_template(template)
        return template.render({"recipient_email": value})
