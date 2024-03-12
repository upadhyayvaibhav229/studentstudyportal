from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class NotesForm(forms.ModelForm):
    class Meta:  # Note the capital "M" in Meta
        model = Notes
        fields = ['title', 'desc']  # Correct field name, should be 'desc' instead of 'description'

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'Due': DateInput()}
        fields = ['Subject','Title', 'Description', 'Due', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length = 100, label = "Enter Your Search: "),



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class Todoform(forms.ModelForm):
    class Meta:
        models = Todo
        fields = ['title', 'is_finished']

        