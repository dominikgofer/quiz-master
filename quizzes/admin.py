from django.contrib import admin
from .models import Category, Quiz, Question, Answer, QuizAttempt, UserAnswer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ('text', 'is_correct', 'order')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'points', 'order')
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'creator', 'is_active', 'is_public', 'created_at')
    list_filter = ('difficulty', 'is_active', 'is_public', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [QuestionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'creator', 'difficulty')
        }),
        ('Quiz Settings', {
            'fields': ('time_limit', 'passing_score', 'max_attempts', 'is_active', 'is_public')
        }),
        ('Display Settings', {
            'fields': ('show_correct_answers', 'randomize_questions', 'randomize_answers')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'quiz', 'question_type', 'points', 'order')
    list_filter = ('question_type', 'quiz')
    search_fields = ('text', 'explanation')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AnswerInline]
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'question_preview', 'is_correct', 'order')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text', 'question__text')
    
    def text_preview(self, obj):
        return obj.text[:40] + '...' if len(obj.text) > 40 else obj.text
    text_preview.short_description = 'Answer'
    
    def question_preview(self, obj):
        return obj.question.text[:40] + '...' if len(obj.question.text) > 40 else obj.question.text
    question_preview.short_description = 'Question'


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'is_correct', 'points_earned', 'answered_at')
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'status', 'score', 'points_earned', 'total_points', 'start_time', 'end_time')
    list_filter = ('status', 'quiz', 'start_time')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('start_time', 'end_time', 'score', 'points_earned', 'total_points')
    inlines = [UserAnswerInline]
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('user', 'quiz', 'status')
        }),
        ('Results', {
            'fields': ('score', 'points_earned', 'total_points')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time')
        }),
    )


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question_preview', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct', 'attempt__quiz')
    search_fields = ('attempt__user__username', 'question__text', 'text_answer')
    readonly_fields = ('answered_at',)
    filter_horizontal = ('selected_answers',)
    
    def question_preview(self, obj):
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Question'
