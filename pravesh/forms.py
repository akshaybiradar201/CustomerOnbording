from django import forms

class UploadForm(forms.Form):
    document = forms.FileField(required=True)