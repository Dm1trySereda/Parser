from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.services.render_template_service.abc import AbstractRenderTemplateService


class RenderTemplateService(AbstractRenderTemplateService):

    async def render_template(self, value: str, template: str):
        env = Environment(
            loader=FileSystemLoader("src/templates/"),
            autoescape=select_autoescape(["html"]),
        )
        template = env.get_template(template)
        email_content = template.render({"recipient_email": value})
        print(template.render())
        return email_content
