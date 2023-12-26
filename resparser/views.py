import os
import json
from uuid import uuid4

from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from .validate import validate
from .parse import extract_data
from .models import ResumeParser
from .forms import ResumeParserForm
from .serializers import ResumeParserSerializer

def generateUniqueName(filename):
    file_name = str(uuid4().hex)[:8]
    extension = filename.split(".")[-1]
    full_name = f"{file_name}.{extension}"
    return full_name


class ResumeParserAPIView(CreateAPIView):
    serializer_class=ResumeParserSerializer
    permission_classes=(AllowAny,)
    def post(self, request, *args, **kwargs):
        
        try:
            # print(request.data)
            file=request.data['file']
            file_name=request.data['file'].name

            # print(file_name)
            fileName = generateUniqueName(file_name)

            # Create a resume parser object and save the file
            obj = ResumeParser.objects.create(file=file, file_name=fileName)
            extracted_data = extract_data(fileName)
            # print('DATA EXTRACTED')
            score_response, issues, checked_data = validate(extracted_data)
            # print('data validated')

            context = {
                "score": score_response,
                "fixes": issues,
                "checked_data": checked_data,
            }

            instance=ResumeParser.objects.get(file_name=fileName)
            instance.delete()

            status_code=status.HTTP_200_OK
            response={
                'success':'True',
                'status':status_code,
                'message':"resume parsed successfully",
                'context':context,
            }
            return Response(response,status=status_code)
        except:
            status_code=status.HTTP_400_BAD_REQUEST
            response={
                'success':'False',
                'status code':status_code,
                'message':"resume parsing failed"
            }
            return Response(response)
            

class ResumeParserView(CreateView):
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
                return render(request, 'success.html', context)
            except Exception as e:
                print(str(e))
                return render(request, 'UploadFile.html', {'error_message': str(e)})
        else:
            return render(request, 'UploadFile.html', {'form': form})


def success(request):
    return render(request, 'success_template.html')