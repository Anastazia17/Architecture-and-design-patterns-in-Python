from jinja2 import Template
import os


def render(template_name, folder='templates', **kwargs):
    file_path = os.path.join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # Рендерим шаблон с параметрами
    return template.render(**kwargs)