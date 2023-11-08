
from django.contrib import admin
from django.urls import path, include
from resparser import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('resparser.urls')),
    path('file/upload/', views.ResumeParserAPIView.as_view(), name ='upload_file'),
    path('success/', views.success, name='success'),

]
