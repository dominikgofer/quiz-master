from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    """Quiz categories for organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Quiz(models.Model):
    """Main quiz model"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='quizzes')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    # Quiz settings
    time_limit = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes")
    passing_score = models.IntegerField(default=70, validators=[MinValueValidator(0), MaxValueValidator(100)], 
                                       help_text="Passing score percentage")
    max_attempts = models.IntegerField(default=3, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    
    # Display settings
    show_correct_answers = models.BooleanField(default=True, help_text="Show correct answers after completion")
    randomize_questions = models.BooleanField(default=False)
    randomize_answers = models.BooleanField(default=False)
    
    # Dates
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def total_points(self):
        """Calculate total points for the quiz"""
        return sum(q.points for q in self.questions.all())
    
    @property
    def is_available(self):
        """Check if quiz is currently available"""
        if not self.is_active:
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
    
    class Meta:
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']


class Question(models.Model):
    """Quiz question model"""
    QUESTION_TYPES = [
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
        ('truefalse', 'True/False'),
        ('text', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='single')
    text = models.TextField()
    explanation = models.TextField(blank=True, help_text="Explanation shown after answer")
    points = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.text[:50]}"
    
    class Meta:
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']


class Answer(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.text[:30]}... - {self.text[:30]}"
    
    class Meta:
        ordering = ['question', 'order']


class QuizAttempt(models.Model):
    """Track user attempts at quizzes"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.status})"
    
    @property
    def is_passed(self):
        """Check if user passed the quiz"""
        if self.score is None:
            return False
        return self.score >= self.quiz.passing_score
    
    @property
    def time_taken(self):
        """Calculate time taken for the attempt"""
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def calculate_score(self):
        """Calculate and save the score for this attempt"""
        correct_answers = self.user_answers.filter(is_correct=True)
        self.points_earned = sum(ua.points_earned for ua in self.user_answers.all())
        self.total_points = self.quiz.total_points
        
        if self.total_points > 0:
            self.score = (self.points_earned / self.total_points) * 100
        else:
            self.score = 0
        
        self.save()
    
    class Meta:
        ordering = ['-start_time']


class UserAnswer(models.Model):
    """Store user's answers to questions"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answers = models.ManyToManyField(Answer, blank=True)
    text_answer = models.TextField(blank=True, help_text="For text-based questions")
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.text[:30]}"
    
    def check_answer(self):
        """Check if the answer is correct and calculate points"""
        if self.question.question_type == 'text':
            # Text answers need manual grading
            self.is_correct = False
            self.points_earned = 0
        elif self.question.question_type == 'truefalse' or self.question.question_type == 'single':
            # Single choice questions
            selected = self.selected_answers.first()
            if selected and selected.is_correct:
                self.is_correct = True
                self.points_earned = self.question.points
            else:
                self.is_correct = False
                self.points_earned = 0
        elif self.question.question_type == 'multiple':
            # Multiple choice questions - all correct answers must be selected
            correct_answers = set(self.question.answers.filter(is_correct=True))
            selected_answers = set(self.selected_answers.all())
            
            if correct_answers == selected_answers:
                self.is_correct = True
                self.points_earned = self.question.points
            else:
                self.is_correct = False
                self.points_earned = 0
        
        self.save()
    
    class Meta:
        ordering = ['answered_at']
        unique_together = ['attempt', 'question']
