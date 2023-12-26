from .models import ResumeParser
from rest_framework import serializers

class ResumeParserSerializer(serializers.Serializer):
    class Meta:
        model = ResumeParser
        fields = ['file']
  

