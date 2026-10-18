from django import forms
from django.utils import text
from .models import Todo

def placeholder(text):
    return forms.TextInput(attrs={'placeholder': text})

class PersonForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Your Name', widget=placeholder('Enter your name'))
    age = forms.IntegerField(label='Your age', widget=placeholder('Enter your age'))
    job = forms.CharField(max_length=100, required=False, label='Your job', widget=placeholder('Enter your job'))


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__' #since we want to define widget for deadline we should type all field manually
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }