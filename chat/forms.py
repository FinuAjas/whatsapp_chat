from django.forms import ModelForm
from django import forms
from . models import *

class ThredForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('first_person', 'second_person')