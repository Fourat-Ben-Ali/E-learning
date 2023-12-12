from django import forms
from platform_app.models import Course,Assignment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'enrollement_capacity', 'tutor']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'course', 'pdf']

    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 