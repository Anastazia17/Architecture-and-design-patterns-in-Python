from wsgiref.simple_server import make_server
from anastazia_framework.main import Framework
from urls import routes, fronts

# Создаем объект WSGI-приложения
application = Framework(routes,fronts)

with make_server('', 8080, application) as httpd:
    print('Запуск на порте 8080...')
    httpd.serve_forever()