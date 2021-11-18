from anastazia_framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server


# Создаем объект WSGI-приложения
application = Framework(routes)

with make_server('', 8080, application) as httpd:
    print('Запуск на порте 8080...')
    httpd.serve_forever()