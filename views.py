from anastazia_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class Guess:
    def __call__(self, request):
        return '200 OK', render('guess.html')


class Puzzle:
    def __call__(self, request):
        return '200 OK', render('puzzle.html')


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'