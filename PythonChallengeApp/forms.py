from django import forms


# For bringing Forms and Models together:
class FileForm(forms.Form):
    ip_file = forms.FileField()
