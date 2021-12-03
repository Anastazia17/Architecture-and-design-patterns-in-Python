from datetime import date
from views import Index, Guess, Puzzle, CreateAnswer, AnswersList, CopyAnswer


# front controller
def secret_front(request):
    request['data'] = date.today()

def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/guess/': Guess(),
    '/puzzle/': Puzzle(),
    '/create_answer/': CreateAnswer(),
    '/answers_list/': AnswersList(),
    '/copy-answer/': CopyAnswer()
}