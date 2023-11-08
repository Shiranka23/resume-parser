from django import forms
from .models import ResumeParser

class ResumeParserForm(forms.ModelForm):
    class Meta:
        model = ResumeParser
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        # Add any custom validation for the uploaded file here, if needed.
        # For example, you can check the file size or file type.
        return file