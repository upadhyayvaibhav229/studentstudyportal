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
        fields = ['Subject','Title', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length = 100, label = "Enter Your Search: "),



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class Todoform(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']


class ConversionForms(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot','Foot')]
    input = forms.CharField(required= False, label= False, widget= forms.TextInput(
        attrs = {'types': 'number', 'placeholder': 'Enter the Number'}
    ))

    measure1 = forms.CharField(

        label= '', widget= forms.Select(choices= CHOICES)
    )
    
    measure2 = forms.CharField(

        label= '', widget= forms.Select(choices= CHOICES)
    )

class ConversionLengthForm(forms.Form):
    LENGTH_CHOICES = [('yard', 'Yard'), ('foot', 'Foot'), ('meter', 'Meter'), ('inch', 'Inch')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.ChoiceField(choices=LENGTH_CHOICES, label='', widget=forms.Select)
    measure2 = forms.ChoiceField(choices=LENGTH_CHOICES, label='', widget=forms.Select)

class ConversionMassForm(forms.Form):
    MASS_CHOICES = [('kilogram', 'Kilogram'), ('pound', 'Pound'), ('gram', 'Gram'), ('ounce', 'Ounce')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.ChoiceField(choices=MASS_CHOICES, label='', widget=forms.Select)
    measure2 = forms.ChoiceField(choices=MASS_CHOICES, label='', widget=forms.Select)
