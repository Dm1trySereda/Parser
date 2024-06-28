from abc import ABC, abstractmethod
from src.enums.template import RenderTemplateChoices


class AbstractRenderTemplateService(ABC):
    @abstractmethod
    async def render_template(self, value: str, template: RenderTemplateChoices):
        pass
