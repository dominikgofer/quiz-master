from django import forms
from .models import Quiz, Question, Answer, Category


class QuizForm(forms.ModelForm):
    """Form for creating and editing quizzes"""
    class Meta:
        model = Quiz
        fields = [
            'title', 'description', 'category', 'difficulty',
            'time_limit', 'passing_score', 'max_attempts',
            'is_active', 'is_public', 'show_correct_answers',
            'randomize_questions', 'randomize_answers',
            'start_date', 'end_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_correct_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'randomize_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'randomize_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class QuestionForm(forms.ModelForm):
    """Form for creating and editing questions"""
    class Meta:
        model = Question
        fields = ['question_type', 'text', 'explanation', 'points', 'order', 'image']
        widgets = {
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AnswerForm(forms.ModelForm):
    """Form for creating and editing answers"""
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'order']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Formsets for managing multiple answers
AnswerFormSet = forms.inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    extra=4,
    can_delete=True,
    min_num=2,
    validate_min=True
)


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., fa-book'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }


class QuizFilterForm(forms.Form):
    """Form for filtering quizzes"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'All Difficulties')] + list(Quiz.DIFFICULTY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search quizzes...'})
    )
