#from django.db import models

# Create your models here.

from __future__ import unicode_literals
from django.db import models

import numpy as np

from django.conf import settings
from django.conf.urls.static import static
from django.core.files.base import ContentFile
from django.db import models

import os
import shutil

#from dicom.dicom_import import dicom_datasets_from_zip, combine_slices
#from dicom.dicom_export import export_to_png

#import zipfile

from datetime import date
import datetime
from django.utils import timezone
from django.utils.timezone import now



class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['first_name'].isalpha()) == False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name can not be shorter than 2 characters"

        if (postData['last_name'].isalpha()) == False:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
"""	
class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    @property
    def voxels(self):
        with self.voxel_file as f:
            voxel_array = np.load(f)
        return voxel_array
    
    @property
    def images_path(self):
        with self.voxel_file as f:
            path = settings.MEDIA_ROOT + "images/" + os.path.basename(f.name)
        return path
    
    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            dicom_datasets = dicom_datasets_from_zip(f)

        voxels, _ = combine_slices(dicom_datasets)
        content_file = ContentFile(b'')  # empty zero byte file
        np.save(content_file, voxels)
        self.voxel_file.save(name='voxels', content=content_file, save=False)
        self._export_pngs(voxels)
        
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID
        super(ImageSeries, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        
        # Delete the images folder as well
        shutil.rmtree(self.images_path)
        
        super(ImageSeries, self).delete(*args, **kwargs)
        
    def _export_pngs(self, voxels):
        path = self.images_path
        if not os.path.exists(path):
            os.makedirs(path)
        
        export_to_png(path, voxels)
        
    class Meta:
        verbose_name_plural = 'Image Series'

"""		
# sample form model
class Contact(models.Model):
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    phone=models.CharField(max_length=20)
    email = models.EmailField()  
    comment = models.CharField(max_length=1000)
	
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


		
		
INSURANCES = (
    (0, "N/A"),
    (1, "Aetna"),
    (2, "United HealthCare"),
    (3, "Humana"),
    (4, "Celtic Healthcare"),
    (5, "BlueCross BlueShield"),
    (6, "Cigna"),
    (7, "Emblem Healthcare"),
    (8, "Amerigroup"),
    (9, "Kaiser Permanente"),
    (10, "Wellpoint"),
)

# Location master 
class Location(models.Model):
    
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    
    def __str__(self):
        return '%s %s' % (self.city, self.state)
	
	
    


class Hospital(models.Model):

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    location = models.ForeignKey(Location, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

 
SPECIALITY = (
    (0, "N/A"),
    (1, "Radiologist"),
    (2, "Neurologist"),
    (3, "Neurosergeon"),
    (4, "Physician"),
    (5, "Pathologist"),
    (6, "Orthopedics"),
    (7, "General Surgery"),
    (8, "Internal Medicine"),
    (9, "Paedriatics"),
    (10, "ENT"),
)
		
class Doctor(models.Model):

	

    GENDER = (
        ('M', "Male"),
        ('F', "Female"),
    )

    @staticmethod
    def toGender(key):
        for item in Profile.GENDER:
            if item[0] == key:
                return item[1]
        return "None"

    
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    speciality = models.IntegerField(max_length=50,choices=SPECIALITY)
    emergencycontactName = models.CharField(blank=True, max_length=50)
    emergencycontactNumber = models.CharField(blank=True, max_length=20)
    sex = models.CharField(blank=True, max_length=1, choices=GENDER)
    birthday = models.DateField(default=date(1900, 1, 1))
    phone = models.CharField( max_length=20)
    created = models.DateTimeField(default=now, editable=False)
    prefHospital = models.ForeignKey(Hospital, blank=True,on_delete=models.CASCADE)

    def get_populated_fields(self):
        """
        This is used by the form to collect the data.
        """
        fields = {}
        if self.firstname is not None:
            fields['firstname'] = self.firstname
        if self.lastname is not None:
            fields['lastname'] = self.lastname
        if self.sex is not None:
            fields['sex'] = self.sex
        if not self.birthday.year == 1000:
            fields['birthday'] = self.birthday
        if self.phone is not None:
            fields['phone'] = self.phone
        
        if self.contactName is not None:
            fields['contactName'] = self.contactName
        if self.contactNumber is not None:
            fields['contactNumber'] = self.emergencycontactNumber
        if self.prefHospital is not None:
            fields['prefHospital'] = self.prefHospital
        return fields

    def __str__(self):
        return self.firstname + " " + self.lastname

 
		
class Patient(models.Model):

	

    GENDER = (
        ('M', "Male"),
        ('F', "Female"),
    )

    @staticmethod
    def toGender(key):
        for item in Profile.GENDER:
            if item[0] == key:
                return item[1]
        return "None"

    
    firstname = models.CharField(blank=True, max_length=50)
    lastname = models.CharField(blank=True, max_length=50)
    insurance = models.IntegerField(max_length=50,choices=INSURANCES)
    prefHospital = models.ForeignKey(Hospital, null=True,on_delete=models.CASCADE)
    emergencyContactName = models.CharField(blank=True, max_length=50)
    emergencyContactNumber = models.CharField(blank=True, max_length=20)
    sex = models.CharField(blank=True, max_length=1, choices=GENDER)
    birthday = models.DateField(default=date(1900, 1, 1))
    phone = models.CharField(blank=True, max_length=20)
    allergies = models.CharField(blank=True, max_length=250)
    created = models.DateTimeField(default=now, editable=False)
    prefHospital = models.ForeignKey(Hospital, null=True,on_delete=models.CASCADE)

    def get_populated_fields(self):
        """
        This is used by the form to collect the data.
        """
        fields = {}
        if self.firstname is not None:
            fields['firstname'] = self.firstname
        if self.lastname is not None:
            fields['lastname'] = self.lastname
		
        if self.insurance is not None:
            fields['insurance'] = self.insurance	
        
        if self.sex is not None:
            fields['sex'] = self.sex
        if not self.birthday.year == 1000:
            fields['birthday'] = self.birthday
        if self.phone is not None:
            fields['phone'] = self.phone
        if self.allergies is not None:
            fields['allergies'] = self.allergies
        
        if self.emergencyContactName is not None:
            fields['emergencyContactName'] = self.emergencyContactName
        if self.emergencyContactNumber is not None:
            fields['emergencyContactNumber'] = self.emergencyContactNumber
        if self.prefHospital is not None:
            fields['prefHospital'] = self.prefHospital
        return fields

    def __str__(self):
        return self.firstname + " " + self.lastname
		
		

class Admission(models.Model):
    
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	time = models.TimeField(default=timezone.now())
	date = models.DateField(default=datetime.date.today())
	reason = models.CharField(max_length=200)
	hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	
	def __str__(self):
	    return '%s %s' % (self.patient, self.date)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today())
    medication = models.CharField(max_length=100)
    strength = models.CharField(max_length=30)
    instruction = models.CharField(max_length=200)
    refill = models.IntegerField()
    active = models.BooleanField(default=True)
	
    def __str__(self):
        return '%s %s' % (self.patient, self.medication, self.strength,)

class MedicalInfo(models.Model):
    BLOOD = (
    ('A+', 'A+ Type'),
    ('B+', 'B+ Type'),
    ('AB+', 'AB+ Type'),
    ('O+', 'O+ Type'),
    ('A-', 'A- Type'),
    ('B-', 'B- Type'),
    ('AB-', 'AB- Type'),
    ('O-', 'O- Type'),
)
    @staticmethod
    def toBlood(key):
        for item in MedicalInfo.BLOOD:
            if item[0] == key:
                return item[1]
        return "None"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bloodType = models.CharField(max_length=10, choices=BLOOD)
    allergy = models.CharField(max_length=100)
    alzheimer = models.BooleanField()
    asthma = models.BooleanField()
    diabetes = models.BooleanField()
    stroke = models.BooleanField()
    comments= models.CharField(max_length=700)

    def get_populated_fields(self):
        fields = {
            'patient': self.patient.account,
            'bloodType': self.bloodType,
            'allergy': self.allergy,
            'alzheimer': self.alzheimer,
            'asthma': self.asthma,
            'diabetes': self.diabetes,
            'stroke': self.stroke,
            'comments': self.comments,
        }
        return fields

class MedicalTest(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today())
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    private = models.BooleanField(default=True)
    completed = models.BooleanField()
    

    def get_populated_fields(self):
        """
        This is used by the form to collect the data.
        """
        fields = {
            'name': self.name,
            'date': self.date,
            'hospital': self.hospital,
            'description': self.description,
            'doctor': self.doctor.account,
            'patient': self.patient.account,
            'private': self.private,
            'completed': self.completed,
            
        }
        return fields


        

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)    
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    startTime = models.TimeField(default=datetime.datetime.now)
    endTime = models.TimeField(default=datetime.datetime.now)
    date = models.DateField(default=datetime.date.today())

    def get_populated_fields(self):
        """
        This is used by the form to collect the data.
        """
        fields = {
            'doctor': self.doctor,
            'patient': self.patient,
            'description': self.description,
            'hospital': self.hospital,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'date': self.date,
        }
        return fields		
		
class PatientFiles(models.Model): 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    title = models.CharField(max_length=50) 
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now())
	
    def __str__(self):
        return self.title