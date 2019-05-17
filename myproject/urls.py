"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


from dicomapp import views
from django.urls import path
from django.conf.urls import url

from django.contrib import admin
from django.urls import path, include 
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from dicomapp import views

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
		
	path('register', views.register, name='register'),
    
	path('login', views.login,name='login'),
	path('logout', views.login,name='logout'),
	
	path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
	path('register', views.register,name='register'),
      
	path('about', views.AboutPageView.as_view(), name='about'),
	path('contact', views.ContactPageView.as_view(), name='contact'),
	path('directions', views.DirectionsPageView.as_view(), name='directions'),
	
	path('send_to_dcom', views.send_to_dcom, name='send_to_dcom'),
    path('medical/app',views.app_render),
    path('medical/process.ajax',views.ajax_server),
	
	path('form_upload', views.FileFieldView.as_view(), name='form_upload'),
	path('patientfiles_upload', views.patientfiles_upload, name = 'patientfiles_upload'),
	#path('dicom_upload', views.dicom_upload, name = 'dicom_upload'),
	path('success', views.MessagePageView.as_view(), name = 'success'),
	#path('dicom_images', views.display_dicom_images, name = 'dicom_images'),
	
	#path('image_series_list', views.image_series_list, name='image_series_list'),
	
    #path('image_series_view', views.image_series_view, name='image_series_view'),
	
	path('contactform', views.contact, name='contactform'),
	
	path('patient_record', views.patient_record, name='patient_record'),
	path('patient_list', views.patient_list, name='patient_list'),
	
	path('patient_medicalinfo', views.patient_medicalinfo, name='patient_medicalinfo'),
	
	path('patient_admission', views.patient_admission, name='patient_admission'),
	#path('patient_admission_list', views.patient_admission_list, name='patient_admission_list'),
	
	path('admission_list', views.admission_list, name='admission_list'),
	
	path('patient_appointment', views.patient_appointment, name='patient_appointment'),
	path('appointment_list', views.appointment_list, name='appointment_list'),
	path('patient_prescription', views.patient_prescription, name='patient_prescription'),
	path('patient_medicaltest', views.patient_medicaltest, name='patient_medicaltest'),
	path('admin/', admin.site.urls),
	path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
	
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
