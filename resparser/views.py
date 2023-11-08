import os
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import ResumeParser
from .forms import ResumeParserForm
from .parse import extract_data
from django.http import HttpResponseRedirect
from django.shortcuts import render
from uuid import uuid4
from .validate import validate

def generateUniqueName(filename):
    file_name = str(uuid4().hex)[:8]
    extension = filename.split(".")[-1]
    full_name = f"{file_name}.{extension}"
    return full_name

class ResumeParserAPIView(CreateView):
    model = ResumeParser
    form_class = ResumeParserForm
    template_name = 'UploadFile.html'
    success_url = reverse_lazy('success')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            file = request.FILES['file']
            file_name = request.FILES['file'].name
            file_extension = file_name.split(".")[-1].lower()
            
            if file_extension not in ['pdf', 'docx']:
                error_message = 'Unsupported file format. Only .pdf and .docx files are accepted.'
                return render(request, 'UploadFile.html', {'error_message': error_message})
            
            fileName = generateUniqueName(file_name)
            
            try:
                doc = ResumeParser.objects.create(
                    file=file,
                    file_name=fileName
                )
                extracted_data = extract_data(fileName)
                score_response, issues, checked_data = validate(extracted_data)
                msg = "Your resume/cv is fit"
                
                if score_response < 66.67:
                    msg = 'This points are missing in your resume/cv'
                
                context = {
                    "score": score_response,
                    "fixes": issues,
                    "msg": msg,
                    "checked_data": checked_data,
                }
                return render(request, 'success_template.html', context)
            except Exception as e:
                print(str(e))
                return render(request, 'UploadFile.html', {'error_message': str(e)})
        else:
            return render(request, 'UploadFile.html', {'form': form})

def success(request):
    return render(request, 'success_template.html')
