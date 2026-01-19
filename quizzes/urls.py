from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    # Public views
    path('', views.home_view, name='home'),
    path('quizzes/', views.quiz_list_view, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail_view, name='quiz_detail'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('leaderboard/<int:pk>/', views.leaderboard_view, name='quiz_leaderboard'),
    
    # Student views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('quiz/<int:pk>/take/', views.quiz_take_view, name='quiz_take'),
    path('quiz/<int:pk>/result/<int:attempt_pk>/', views.quiz_result_view, name='quiz_result'),
    path('history/', views.quiz_history_view, name='quiz_history'),
    
    # Teacher views - Quiz management
    path('quiz/create/', views.quiz_create_view, name='quiz_create'),
    path('quiz/<int:pk>/edit/', views.quiz_edit_view, name='quiz_edit'),
    path('quiz/<int:pk>/delete/', views.quiz_delete_view, name='quiz_delete'),
    path('quiz/<int:pk>/questions/', views.quiz_manage_questions_view, name='quiz_manage_questions'),
    path('quiz/<int:pk>/reports/', views.quiz_reports_view, name='quiz_reports'),
    
    # Teacher views - Question management
    path('quiz/<int:quiz_pk>/question/create/', views.question_create_view, name='question_create'),
    path('question/<int:pk>/edit/', views.question_edit_view, name='question_edit'),
    path('question/<int:pk>/delete/', views.question_delete_view, name='question_delete'),
]
