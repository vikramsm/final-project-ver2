from django_tables2 import tables, TemplateColumn
from dicomapp.models import Patient, Admission, Appointment

class PatientTable(tables.Table):
    class Meta:
        model = Patient
        template_name = 'django_tables2/bootstrap.html'
        #attrs = {'class':'table table-sm'}
        #fields = ['ID' ,'Firstname', 'Lastname', 'EmergencyContactName', 'EmergencyContactNumber', 'Sex', 'Birthday', 'Phone', 'Allergies', 'Created', 'PrefHospital'] 
	
        #edit = TemplateColumn(template_name='training_update_column.html')
		

class AdmissionTable(tables.Table):
    class Meta:
        model = Admission
        template_name = 'django_tables2/bootstrap.html'
		#attrs = {'class':'table table-sm'}
        #fields = ['ID' ,'Patient', 'Time', 'Date', 'Reason', 'PrefHospital','Active'] 
	
        #edit = TemplateColumn(template_name='training_update_column.html')
		
class AppointmentTable(tables.Table):
    class Meta:
        model = Appointment
        template_name = 'django_tables2/bootstrap.html'