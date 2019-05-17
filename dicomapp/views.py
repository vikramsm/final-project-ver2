from django.shortcuts import render

# Create your views here.

import base64
import os
import time
import traceback
from io import BytesIO

import imageio
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from termcolor import colored
from django.urls import reverse
from myproject import settings
from django.views.generic import TemplateView
#####
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import *
from django.views.generic.edit import FormView
from .forms import FileFieldForm

#from .models import ImageSeries
from django.core.exceptions import ObjectDoesNotExist

from dicomapp.models import Location, Hospital, Doctor, Patient, MedicalInfo,Prescription, Admission, Appointment, MedicalTest,Contact
from django.http import HttpResponseRedirect


from django_tables2 import RequestConfig
from .tables import PatientTable, AdmissionTable, AppointmentTable

from django.contrib.auth import views as auth_views


def index(request):
    return render(request, 'index.html')


	
def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    if (User.objects.filter(email=request.POST['login_email']).exists()):
        user = User.objects.filter(email=request.POST['login_email'])[0]
        if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):
            request.session['id'] = user.id
            return redirect('/success')
    return redirect('/')


# Static page for About us
class AboutPageView(TemplateView):
    template_name = 'about.html'	

# Static page for Contact us
class ContactPageView(TemplateView):
    template_name = 'contact.html'	
	
	
# Static page for directions
class DirectionsPageView(TemplateView):
    template_name = 'directions.html'

# Static page for Message display
class MessagePageView(TemplateView):
    template_name = 'messages.html'	
	

#######
# Image rendering
def send_to_dcom(request):
   return redirect('medical/app')


def ajax_server(request):
    start = time.time()
    d = dict()
    generic = dict()
    medinfo = dict()

    try:

        print('FILE--->',str(request.FILES['imgInp'])[-3:])

        if request.method == 'POST' and ('imgInp' in request.FILES) and request.FILES['imgInp'] and  str(request.FILES['imgInp'])[-3:].upper() =='DCM':
            file = request.FILES['imgInp']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            full_path_file = os.path.join(settings.MEDIA_ROOT, filename)
            print(colored('path->', 'red'), full_path_file)

            generic['name'] = filename
            generic['size'] = os.path.getsize(full_path_file)
            try:
                if full_path_file[-3:].upper() == 'DCM':
                    dcpimg = imageio.imread(full_path_file)
                    for keys in dcpimg.meta:

                        medinfo[keys] = str(dcpimg.meta[keys])

                    if len(dcpimg.shape) ==4:
                        dcpimg = dcpimg[0,0]
                    elif len(dcpimg.shape) ==3:
                        dcpimg = dcpimg[0]

                    fig = plt.gcf()
                    fig.set_size_inches(18.5, 10.5)
                    plt.imshow(dcpimg, cmap='gray')
                    plt.colorbar()
                    figure = BytesIO()
                    plt.savefig(figure, format='jpg', dpi=300)

                    plt.close()
                    d['url'] = {'base64': 'data:image/png;base64,' + base64.b64encode(figure.getvalue()).decode()}

                # medinfo.update(dcpimg.meta)

            except Exception as e:

                traceback.print_tb(e)





            fs.delete(filename)
    except Exception as e:
        traceback.print_tb(e)




    generic['process time'] = time.time() - start
    d['generic'] = generic


    d['med'] = medinfo


    print(colored(d, 'red'))
    return JsonResponse(d)





def app_render(request):
    print(settings.BASE_DIR)
    d = {'title': 'DICOM viewer','info':'DICOM SERVER SIDE RENDER'}
    return render(request, "main_template.html", d)


# view for uploading images 	
class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'form_upload.html'  # Replace with  template.
    success_url = 'form_upload.html'  # Replace with URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


			
# view for uploading images 
def patientfiles_upload(request): 
  
    if request.method == 'POST': 
        form = PatientFilesForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = FileFieldForm() 
    return render(request, 'patientfiles_upload.html', {'form' : form}) 


	
def success(request): 
    return HttpResponse('successfuly uploaded') 
	
# view for displaying images 
def display_dicom_images(request):
    Dicom=None 
    
    if request.method == 'GET': 
	# getting all the objects of hotel. 
	    Dicom = Dicom.objects.all()  
	    return render((request, 'display_dicom_images.html',{'dicom_images' : Dicom}))

"""		
def image_series_list(request):
    return render(request, 'image_series_list.html', {
        'all_image_series': ImageSeries.objects.all(),
    })

def image_series_view(request, id):
    series = ImageSeries.objects.get(id=id)
    voxels = series.voxels
    
    return render(request, 'image_series_view.html', {
        'series': series,
        'voxels': voxels,
    })

"""
# View for contact us form
def contact(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = ContactForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('success.html')
    else:
        # GET, generate unbound (blank) form
        form = ContactForm()
    return render(request,'contactform.html',{'form':form})



# View for  Patient Record  
def patient_record(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = PatientForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            #messages.success(request,'Successful!')
            return render(request,"messages.html")
            #return messages.success(request, 'messages')
            # redirect to a new URL:
            #return HttpResponseRedirect(request,'success')
            
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        # GET, generate unbound (blank) form
        form = PatientForm()
    return render(request,'patient_record.html',{'form':form})	

	
# View for patient admission
def patient_admission(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = PatientAdmissionForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            return render(request,"admission_success_message.html")
			#return reverse('messages')
            #return messages.success(request, 'messages')
            # redirect to a new URL:
            #return HttpResponseRedirect(request,'success')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        # GET, generate unbound (blank) form
        form = PatientAdmissionForm()
    return render(request,'patient_admission.html',{'form':form})
	

# View for List of patient admissions
def patient_admission_list(request):
    return render(request, 'patient_admission_list.html', {'patient_admission': Admission.objects.all()})
"""	
# View for List of patient admissions
def admission_list(request):
    return render(request, 'admission_list.html', {'admission': Admission.objects.all()})
"""
	
# View for patient appointment
def patient_appointment(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = PatientAppointmentForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            return render(request,"appointment_success_message.html")
			#return messages.success(request, 'messages')
            # redirect to a new URL:
            #return HttpResponseRedirect(request,'messages')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        # GET, generate unbound (blank) form
        form = PatientAppointmentForm()
    return render(request,'patient_appointment.html',{'form':form})


# View for patient prescriptions
def patient_prescription(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = PatientPrescriptionForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            return render(request,"prescription_success_message.html")
			#return messages.success(request, 'messages')
            # redirect to a new URL:
            #return HttpResponseRedirect(request,'messages')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        # GET, generate unbound (blank) form
        form = PatientPrescriptionForm()
    return render(request,'patient_prescription.html',{'form':form})


# View forpatient medical information	
def patient_medicalinfo(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = MedicalInfoForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            return render(request,"medicalinfo_success_message.html")
            #return messages.success(request, 'messages')
            # redirect to a new URL:
            #return HttpResponseRedirect(request,'messages')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        # GET, generate unbound (blank) form
        form = MedicalInfoForm()
    return render(request,'patient_medicalinfo.html',{'form':form})	

	
# View for patient medical tests
def patient_medicaltest(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = PatientMedicalTestForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            return render(request,"medicaltest_success_message.html")
            #return messages.success(request, 'messages')
            # redirect to a new URL:
            #return HttpResponseRedirect(request,'messages')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        # GET, generate unbound (blank) form
        form = PatientMedicalTestForm()
    return render(request,'patient_medicaltest.html',{'form':form})
	
# View for List of patient admissions
def patient_list(request):
    table = PatientTable(Patient.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'patient_list.html', {'table': table})

	
def admission_list(request):
    table = AdmissionTable(Admission.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'admission_list.html', {'table': table})

def appointment_list(request):
    table = AppointmentTable(Admission.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'appointment_list.html', {'table': table})	