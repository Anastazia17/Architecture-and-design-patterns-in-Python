from datetime import date

from simba_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    TemplateView, ListView, CreateView, BaseSerializer


site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}

# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.answers)


# контроллер "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


# контроллер - Расписания
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# контроллер 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            answer = site.find_answer_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=answer.courses, name=answer.name, id=answer.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    answer_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            answer = None
            if self.answer_id != -1:
                answer = site.find_answer_by_id(int(self.answer_id))

                course = site.create_course('record', name, answer)
                # Добавляем наблюдателей на курс
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=answer.courses,
                                    name=answer.name, id=answer.id)

        else:
            self.answer_id = int(request['request_params']['id'])
            answer = site.find_answer_by_id(int(self.answer_id))

            return '200 OK', render('create_course.html', name=answer.name, id=answer.id)


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-answer/')
class CreateAnswer:
    @Debug(name='CreateAnswer')
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


# контроллер - список категорий
@AppRoute(routes=routes, url='/answer-list/')
class AnswerList:
    @Debug(name='AnswerList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('answer_list.html', objects_list=site.answers)


# контроллер - копировать курс
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()