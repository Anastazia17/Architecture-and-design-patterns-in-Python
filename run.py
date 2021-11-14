from wsgiref.simple_server import make_server
from Anastazia_Framework import Framework
from urls import routes


# Создаем объект WSGI-приложения
application = Framework(routes)

with make_server('', 8080, application) as httpd:
    print('Запуск на порте 8080...')
    httpd.serve_forever()