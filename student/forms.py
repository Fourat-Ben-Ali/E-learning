from django import forms
from platform_app.models import Enrollment

class EnrollmentForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur')