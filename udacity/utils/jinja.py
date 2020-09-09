import json
import os

import markdown
from jinja2 import Undefined, Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from slug import slug


def duration(mins):
    return f"{mins // 60}h {mins % 60}m"


class SilentUndefined(Undefined):
    """
    Don't break page loads because vars aren't there!
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        print(f'JINJA2: `{self._undefined_name}` was undefined!')
        return None


dir_path = os.path.dirname(os.path.realpath(__file__))
templates_dir = os.path.join(dir_path, '..', 'templates')

jinjaEnv = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(['html', 'xml']),
    undefined=SilentUndefined,
)

md = markdown.Markdown(extensions=['meta'])
jinjaEnv.filters['markdown'] = lambda text: Markup(md.convert(text))
jinjaEnv.filters['json'] = lambda text: json.dumps(text, indent=4)
jinjaEnv.globals['slug'] = slug
jinjaEnv.filters['duration'] = duration
