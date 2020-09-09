import os

from .jinja import jinjaEnv
from .object_dict import ObjectDict


class Renderer(ObjectDict):
    def render(self, file_path, **kwargs):
        return jinjaEnv.get_template(file_path).render(**kwargs)

    def render_page(self, file_path, title, **kwargs):
        return jinjaEnv.get_template('_layout.html') \
            .render(title=title, template=file_path, **kwargs)


class AtomRenderer(Renderer):
    def render(self, **kwargs):
        file_path = os.path.join('atoms', self.__class__.__name__ + '.html')
        return super().render(file_path, atom=self, **kwargs)

    def render_page(self, **kwargs):
        file_path = os.path.join('atoms', self.__class__.__name__ + '.html')
        return super().render_page(file_path, self.title, atom=self, **kwargs)


class ClassRenderer(Renderer):
    def render(self, **kwargs):
        file_path = os.path.join(self.__class__.__name__ + '.html')
        return super().render(file_path, **{self.__class__.__name__.lower(): self}, **kwargs)

    def render_page(self, **kwargs):
        file_path = os.path.join(self.__class__.__name__ + '.html')
        return super().render_page(file_path, self.title, **{self.__class__.__name__.lower(): self}, **kwargs)
