from django import forms
from django.core import validators
from PythonChallengeApp.models import InputFile


# For bringing Forms and Models together:
class FileForm(forms.ModelForm):
    names = forms.CharField(validators=[validators.MinLengthValidator(1)])

    class Meta:
        model = InputFile
        exclude = ()

