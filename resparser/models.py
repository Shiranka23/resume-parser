from django.db import models

def upload_location(instance,filename):
    return 'documents/%s' % (instance.file_name)


class ResumeParser(models.Model):
    file_name=models.CharField(max_length=50,null=False,blank=False)
    file  = models.FileField(upload_to=upload_location)
    uploaded_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.file_name}"