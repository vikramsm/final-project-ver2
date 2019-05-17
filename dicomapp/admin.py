from django.contrib import admin

# Register your models here.

from dicomapp.models import Location, Hospital, Location, Doctor, Patient, Admission, Appointment, Prescription, MedicalInfo, MedicalTest,PatientFiles 

admin.site.register(Location)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Admission)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(MedicalInfo)
admin.site.register(MedicalTest)
admin.site.register(PatientFiles)