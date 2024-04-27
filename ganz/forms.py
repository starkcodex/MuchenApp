import datetime
from django import forms
from .models import Todo
from django.forms.fields import DateField


class TodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ['title', 'description','task_started','task_ended' ,'is_completed']