from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quizzes.models import Category, Quiz, Question, Answer
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create users
        teacher, created = User.objects.get_or_create(
            username='teacher',
            defaults={
                'email': 'teacher@example.com',
                'first_name': 'John',
                'last_name': 'Teacher',
                'is_staff': False
            }
        )
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            teacher.profile.role = 'teacher'
            teacher.profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created teacher: {teacher.username}'))
        
        student, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@example.com',
                'first_name': 'Jane',
                'last_name': 'Student',
                'is_staff': False
            }
        )
        if created:
            student.set_password('student123')
            student.save()
            student.profile.role = 'student'
            student.profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created student: {student.username}'))
        
        # Create categories
        categories_data = [
            {'name': 'Python', 'description': 'Python programming quizzes', 'icon': 'fa-python', 'color': '#3776ab'},
            {'name': 'JavaScript', 'description': 'JavaScript quizzes', 'icon': 'fa-js', 'color': '#f7df1e'},
            {'name': 'Web Development', 'description': 'HTML, CSS, and Web Development', 'icon': 'fa-code', 'color': '#e34c26'},
            {'name': 'Databases', 'description': 'SQL and Database quizzes', 'icon': 'fa-database', 'color': '#336791'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat.name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))
        
        # Create sample quiz
        quiz, created = Quiz.objects.get_or_create(
            title='Python Basics Quiz',
            defaults={
                'description': 'Test your knowledge of Python fundamentals',
                'category': categories['Python'],
                'creator': teacher,
                'difficulty': 'easy',
                'time_limit': 15,
                'passing_score': 70,
                'max_attempts': 3,
                'is_active': True,
                'is_public': True,
                'show_correct_answers': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created quiz: {quiz.title}'))
            
            # Create questions for the quiz
            questions_data = [
                {
                    'text': 'What is the output of print(2 + 3)?',
                    'question_type': 'single',
                    'points': 10,
                    'order': 1,
                    'answers': [
                        {'text': '5', 'is_correct': True},
                        {'text': '23', 'is_correct': False},
                        {'text': 'Error', 'is_correct': False},
                        {'text': 'None', 'is_correct': False},
                    ]
                },
                {
                    'text': 'Which of the following are valid Python data types? (Select all that apply)',
                    'question_type': 'multiple',
                    'points': 10,
                    'order': 2,
                    'answers': [
                        {'text': 'int', 'is_correct': True},
                        {'text': 'string', 'is_correct': False},
                        {'text': 'str', 'is_correct': True},
                        {'text': 'float', 'is_correct': True},
                    ]
                },
                {
                    'text': 'Python is a compiled language.',
                    'question_type': 'truefalse',
                    'points': 10,
                    'order': 3,
                    'answers': [
                        {'text': 'True', 'is_correct': False},
                        {'text': 'False', 'is_correct': True},
                    ]
                },
                {
                    'text': 'Which keyword is used to define a function in Python?',
                    'question_type': 'single',
                    'points': 10,
                    'order': 4,
                    'answers': [
                        {'text': 'function', 'is_correct': False},
                        {'text': 'def', 'is_correct': True},
                        {'text': 'func', 'is_correct': False},
                        {'text': 'define', 'is_correct': False},
                    ]
                },
            ]
            
            for q_data in questions_data:
                answers_data = q_data.pop('answers')
                question = Question.objects.create(quiz=quiz, **q_data)
                
                for i, a_data in enumerate(answers_data):
                    Answer.objects.create(question=question, order=i, **a_data)
                
                self.stdout.write(self.style.SUCCESS(f'Created question: {question.text[:50]}...'))
        
        # Create another quiz
        quiz2, created = Quiz.objects.get_or_create(
            title='JavaScript Fundamentals',
            defaults={
                'description': 'Test your JavaScript knowledge',
                'category': categories['JavaScript'],
                'creator': teacher,
                'difficulty': 'medium',
                'time_limit': 20,
                'passing_score': 75,
                'max_attempts': 2,
                'is_active': True,
                'is_public': True,
                'show_correct_answers': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created quiz: {quiz2.title}'))
            
            questions_data = [
                {
                    'text': 'What does "typeof null" return in JavaScript?',
                    'question_type': 'single',
                    'points': 10,
                    'order': 1,
                    'answers': [
                        {'text': 'null', 'is_correct': False},
                        {'text': 'undefined', 'is_correct': False},
                        {'text': 'object', 'is_correct': True},
                        {'text': 'number', 'is_correct': False},
                    ]
                },
                {
                    'text': 'JavaScript is a statically typed language.',
                    'question_type': 'truefalse',
                    'points': 10,
                    'order': 2,
                    'answers': [
                        {'text': 'True', 'is_correct': False},
                        {'text': 'False', 'is_correct': True},
                    ]
                },
            ]
            
            for q_data in questions_data:
                answers_data = q_data.pop('answers')
                question = Question.objects.create(quiz=quiz2, **q_data)
                
                for i, a_data in enumerate(answers_data):
                    Answer.objects.create(question=question, order=i, **a_data)
                
                self.stdout.write(self.style.SUCCESS(f'Created question: {question.text[:50]}...'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created Successfully ==='))
        self.stdout.write(self.style.SUCCESS('Teacher account: username=teacher, password=teacher123'))
        self.stdout.write(self.style.SUCCESS('Student account: username=student, password=student123'))
