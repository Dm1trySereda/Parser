from abc import ABC, abstractmethod


class AbstractRenderTemplateService(ABC):
    @abstractmethod
    async def render_template(self, value: str, template: str):
        pass
