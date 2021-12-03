from datetime import date
from anastazia_framework.templator import render
from patterns.сreational_patterns import Engine, Logger


site = Engine()
logger = Logger('main')


# Контроллер - Главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=date.today(), objects_list=site.answers)


# Контроллер - Игра Угадайка
class Guess:
    def __call__(self, request):
        return '200 OK', render('guess.html')


# Контроллер - Игра Загадки
class Puzzle:
    def __call__(self, request):
        return '200 OK', render('puzzle.html')


# Контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Контроллер - создать ответ в игре
class CreateAnswer:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            answer_id = data.get('answer_id')

            answer = None
            if answer_id:
                answer = site.find_answer_by_id(int(answer_id))

            new_answer = site.create_answer(name, answer)

            site.answers.append(new_answer)

            return '200 OK', render('index.html', objects_list=site.answers)
        else:
            answers = site.answers
            return '200 OK', render('create_answer.html', answers=answers)


# Контроллер - список ответов
class AnswersList:
    def __call__(self, request):
        logger.log('Список ответов')
        return '200 OK', render('answers_list.html', objects_list=site.answers)


# Контроллер - копировать ответ
class CopyAnswer:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_answer = site.get_answer(name)
            if old_answer:
                new_name = f'copy_{name}'
                new_answer = old_answer.clone()
                new_answer.name = new_name
                site.answers.append(new_answer)

            return '200 OK', render('answers_list.html', objects_list=site.answers)
        except KeyError:
            return '200 OK', 'No answers have been added yet'