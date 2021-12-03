import copy
import quopri


# Абстрактный пользователь
class User:
    pass


# Проверяющий
class Reviewer(User):
    pass


# Игрок
class Player(User):
    pass


# Порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'reviewer': Reviewer,
        'player': Player
    }

    # Порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# Ответы
class Answer:
    # Реестр:
    auto_id = 0

    def __init__(self, name, answer):
        self.id = Answer.auto_id
        Answer.auto_id += 1
        self.name = name
        self.answer = answer
        self.answers = []

    def answers_count(self):
        result = len(self.answers)
        if self.answer:
            result += self.answer.answers_count()
        return result


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.reviewers = []
        self.players = []
        self.answers = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_answer(name, answer=None):
        return Answer(name, answer)

    def find_answer_by_id(self, id):
        for item in self.answers:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет ответа с id = {id}')


# Порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)