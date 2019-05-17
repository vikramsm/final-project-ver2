from django import forms
from .models import *

from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from dicomapp.models import  Location, Hospital, Doctor, Patient, Admission, MedicalInfo, Prescription, Appointment


# Form for uploading files
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	

# Form for uploading patient files 
class PatientFilesForm(forms.ModelForm): 
    class Meta: 
        model = PatientFiles 
        fields = '__all__'

# Contact form for general enquiries
class ContactForm(forms.ModelForm):
      class Meta:      
            model = Contact
            fields = '__all__'

# Form for registering new patient			
class PatientForm(forms.ModelForm):
      class Meta:      
            model = Patient
            fields = '__all__'

class PatientListForm(forms.ModelForm):
      class Meta:      
            model = Patient
            fields = '__all__'			
			
# Form for patient medical informtion			
class MedicalInfoForm(forms.ModelForm):
      class Meta:      
            model = MedicalInfo
            fields = '__all__'
			

# Form for patient admissions
class PatientAdmissionForm(forms.ModelForm):
      class Meta:      
            model = Admission
            fields = '__all__'

# Form for patient admissions list			
class PatientAdmissionListForm(forms.ModelForm):
      class Meta:      
            model = Admission
            fields = '__all__'

# Form for patient appointments
class PatientAppointmentForm(forms.ModelForm):
      class Meta:      
            model = Appointment
            fields = '__all__'

# Form for patient prescriptions
class PatientPrescriptionForm(forms.ModelForm):
      class Meta:      
            model = Prescription
            fields = '__all__'

# Form for patient tests
class PatientMedicalTestForm(forms.ModelForm):
      class Meta:      
            model = MedicalTest
            fields = '__all__'
			
