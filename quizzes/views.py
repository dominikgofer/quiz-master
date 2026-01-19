from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.http import JsonResponse
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer, Category
from .forms import QuizForm, QuestionForm, AnswerFormSet, CategoryForm, QuizFilterForm
import random


def home_view(request):
    """Homepage with featured quizzes"""
    featured_quizzes = Quiz.objects.filter(is_active=True, is_public=True)[:6]
    categories = Category.objects.all()
    
    context = {
        'featured_quizzes': featured_quizzes,
        'categories': categories,
    }
    return render(request, 'quizzes/home.html', context)


@login_required
def dashboard_view(request):
    """User dashboard"""
    user = request.user
    
    if user.profile.role == 'teacher':
        # Teacher dashboard
        created_quizzes = Quiz.objects.filter(creator=user)
        total_attempts = QuizAttempt.objects.filter(quiz__creator=user).count()
        
        context = {
            'is_teacher': True,
            'created_quizzes': created_quizzes,
            'total_attempts': total_attempts,
        }
    else:
        # Student dashboard
        recent_attempts = QuizAttempt.objects.filter(user=user).order_by('-start_time')[:5]
        available_quizzes = Quiz.objects.filter(is_active=True, is_public=True).exclude(
            attempts__user=user, attempts__status='completed'
        )[:6]
        
        # Calculate statistics
        completed_attempts = QuizAttempt.objects.filter(user=user, status='completed')
        avg_score = completed_attempts.aggregate(Avg('score'))['score__avg'] or 0
        
        context = {
            'is_teacher': False,
            'recent_attempts': recent_attempts,
            'available_quizzes': available_quizzes,
            'total_completed': completed_attempts.count(),
            'avg_score': round(avg_score, 1),
        }
    
    return render(request, 'quizzes/dashboard.html', context)


def quiz_list_view(request):
    """Browse all available quizzes"""
    quizzes = Quiz.objects.filter(is_active=True, is_public=True)
    
    # Apply filters
    filter_form = QuizFilterForm(request.GET)
    if filter_form.is_valid():
        category = filter_form.cleaned_data.get('category')
        difficulty = filter_form.cleaned_data.get('difficulty')
        search = filter_form.cleaned_data.get('search')
        
        if category:
            quizzes = quizzes.filter(category=category)
        if difficulty:
            quizzes = quizzes.filter(difficulty=difficulty)
        if search:
            quizzes = quizzes.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
    
    context = {
        'quizzes': quizzes,
        'filter_form': filter_form,
    }
    return render(request, 'quizzes/quiz_list.html', context)


def quiz_detail_view(request, pk):
    """Quiz detail page"""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    # Check if user has attempts
    user_attempts = None
    attempts_left = quiz.max_attempts
    if request.user.is_authenticated:
        user_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz, status='completed')
        attempts_left = quiz.max_attempts - user_attempts.count()
    
    context = {
        'quiz': quiz,
        'user_attempts': user_attempts,
        'attempts_left': attempts_left,
        'can_attempt': attempts_left > 0 if request.user.is_authenticated else False,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def quiz_take_view(request, pk):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    # Check if quiz is available
    if not quiz.is_available:
        messages.error(request, 'This quiz is not currently available.')
        return redirect('quizzes:quiz_detail', pk=pk)
    
    # Check attempts
    completed_attempts = QuizAttempt.objects.filter(
        user=request.user, quiz=quiz, status='completed'
    ).count()
    
    if completed_attempts >= quiz.max_attempts:
        messages.error(request, 'You have used all your attempts for this quiz.')
        return redirect('quizzes:quiz_detail', pk=pk)
    
    # Get or create in-progress attempt
    attempt, created = QuizAttempt.objects.get_or_create(
        user=request.user,
        quiz=quiz,
        status='in_progress',
        defaults={'total_points': quiz.total_points}
    )
    
    # Get questions
    questions = list(quiz.questions.all())
    if quiz.randomize_questions:
        random.shuffle(questions)
    
    if request.method == 'POST':
        # Process answers
        for question in questions:
            answer_key = f'question_{question.id}'
            
            # Get or create user answer
            user_answer, _ = UserAnswer.objects.get_or_create(
                attempt=attempt,
                question=question
            )
            
            if question.question_type == 'text':
                user_answer.text_answer = request.POST.get(answer_key, '')
            elif question.question_type == 'multiple':
                # Multiple choice - get list of selected answers
                selected_ids = request.POST.getlist(answer_key)
                user_answer.selected_answers.set(Answer.objects.filter(id__in=selected_ids))
            else:
                # Single choice or true/false
                selected_id = request.POST.get(answer_key)
                if selected_id:
                    user_answer.selected_answers.set([Answer.objects.get(id=selected_id)])
            
            user_answer.check_answer()
        
        # Complete the attempt
        attempt.status = 'completed'
        attempt.end_time = timezone.now()
        attempt.calculate_score()
        
        messages.success(request, f'Quiz completed! Your score: {attempt.score:.1f}%')
        return redirect('quizzes:quiz_result', pk=pk, attempt_pk=attempt.pk)
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt,
    }
    return render(request, 'quizzes/quiz_take.html', context)


@login_required
def quiz_result_view(request, pk, attempt_pk):
    """View quiz results"""
    quiz = get_object_or_404(Quiz, pk=pk)
    attempt = get_object_or_404(QuizAttempt, pk=attempt_pk, quiz=quiz)
    
    # Check ownership
    if attempt.user != request.user and quiz.creator != request.user:
        messages.error(request, 'You do not have permission to view this result.')
        return redirect('quizzes:dashboard')
    
    user_answers = attempt.user_answers.all().select_related('question')
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'user_answers': user_answers,
        'show_answers': quiz.show_correct_answers,
    }
    return render(request, 'quizzes/quiz_result.html', context)


@login_required
def quiz_history_view(request):
    """View user's quiz history"""
    attempts = QuizAttempt.objects.filter(
        user=request.user, status='completed'
    ).select_related('quiz').order_by('-start_time')
    
    context = {
        'attempts': attempts,
    }
    return render(request, 'quizzes/quiz_history.html', context)


# Teacher views
@login_required
def quiz_create_view(request):
    """Create a new quiz (teacher only)"""
    if request.user.profile.role != 'teacher':
        messages.error(request, 'You must be a teacher to create quizzes.')
        return redirect('quizzes:dashboard')
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('quizzes:quiz_manage_questions', pk=quiz.pk)
    else:
        form = QuizForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'quizzes/quiz_form.html', context)


@login_required
def quiz_edit_view(request, pk):
    """Edit a quiz (teacher only)"""
    quiz = get_object_or_404(Quiz, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quizzes:quiz_detail', pk=pk)
    else:
        form = QuizForm(instance=quiz)
    
    context = {'form': form, 'quiz': quiz, 'action': 'Edit'}
    return render(request, 'quizzes/quiz_form.html', context)


@login_required
def quiz_delete_view(request, pk):
    """Delete a quiz (teacher only)"""
    quiz = get_object_or_404(Quiz, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('quizzes:dashboard')
    
    context = {'quiz': quiz}
    return render(request, 'quizzes/quiz_confirm_delete.html', context)


@login_required
def quiz_manage_questions_view(request, pk):
    """Manage questions for a quiz (teacher only)"""
    quiz = get_object_or_404(Quiz, pk=pk, creator=request.user)
    questions = quiz.questions.all().order_by('order')
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/quiz_manage_questions.html', context)


@login_required
def question_create_view(request, quiz_pk):
    """Create a question for a quiz (teacher only)"""
    quiz = get_object_or_404(Quiz, pk=quiz_pk, creator=request.user)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        answer_formset = AnswerFormSet(request.POST)
        
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            answers = answer_formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            
            messages.success(request, 'Question created successfully!')
            return redirect('quizzes:quiz_manage_questions', pk=quiz_pk)
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
    
    context = {
        'quiz': quiz,
        'question_form': question_form,
        'answer_formset': answer_formset,
        'action': 'Create',
    }
    return render(request, 'quizzes/question_form.html', context)


@login_required
def question_edit_view(request, pk):
    """Edit a question (teacher only)"""
    question = get_object_or_404(Question, pk=pk)
    quiz = question.quiz
    
    if quiz.creator != request.user:
        messages.error(request, 'You do not have permission to edit this question.')
        return redirect('quizzes:dashboard')
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        answer_formset = AnswerFormSet(request.POST, instance=question)
        
        if question_form.is_valid() and answer_formset.is_valid():
            question_form.save()
            answer_formset.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('quizzes:quiz_manage_questions', pk=quiz.pk)
    else:
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerFormSet(instance=question)
    
    context = {
        'quiz': quiz,
        'question': question,
        'question_form': question_form,
        'answer_formset': answer_formset,
        'action': 'Edit',
    }
    return render(request, 'quizzes/question_form.html', context)


@login_required
def question_delete_view(request, pk):
    """Delete a question (teacher only)"""
    question = get_object_or_404(Question, pk=pk)
    quiz = question.quiz
    
    if quiz.creator != request.user:
        messages.error(request, 'You do not have permission to delete this question.')
        return redirect('quizzes:dashboard')
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('quizzes:quiz_manage_questions', pk=quiz.pk)
    
    context = {'question': question, 'quiz': quiz}
    return render(request, 'quizzes/question_confirm_delete.html', context)


@login_required
def quiz_reports_view(request, pk):
    """View quiz reports and analytics (teacher only)"""
    quiz = get_object_or_404(Quiz, pk=pk, creator=request.user)
    
    attempts = QuizAttempt.objects.filter(quiz=quiz, status='completed')
    
    # Calculate statistics
    stats = attempts.aggregate(
        total_attempts=Count('id'),
        avg_score=Avg('score'),
    )
    
    # Get recent attempts
    recent_attempts = attempts.order_by('-end_time')[:10]
    
    context = {
        'quiz': quiz,
        'stats': stats,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quizzes/quiz_reports.html', context)


def leaderboard_view(request, pk=None):
    """View leaderboard for a quiz or overall"""
    if pk:
        quiz = get_object_or_404(Quiz, pk=pk)
        attempts = QuizAttempt.objects.filter(
            quiz=quiz, status='completed'
        ).order_by('-score', 'end_time')[:10]
        context = {'quiz': quiz, 'attempts': attempts}
    else:
        # Overall leaderboard - best average score
        from django.db.models import Avg
        users_scores = QuizAttempt.objects.filter(
            status='completed'
        ).values('user__username').annotate(
            avg_score=Avg('score'),
            total_quizzes=Count('quiz', distinct=True)
        ).order_by('-avg_score')[:10]
        context = {'users_scores': users_scores}
    
    return render(request, 'quizzes/leaderboard.html', context)
