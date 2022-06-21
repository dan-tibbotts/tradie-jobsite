from django import forms
from projects.models import *
from django.forms.models import ModelForm
from projects.models import *

class ProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['customer_id', 'name', 'location', 'status']
        widgets = {
            'customer_id': forms.Select(attrs={
                'class':'form-control form-control-user',
                'required': True
                }),
            'name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Project Name',
                'required': True
                }),
            'location': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Location',
                }),
            'status': forms.Select(attrs={
                'class':'form-control form-control-user col-lg-3 sm-12',
                'required': True
                }),
        }
        error_messages = {
            'customer_id': {
                'required': 'You must select a customer'
            },
            'name': {
                'required': 'You must enter a project name'
            },
        
        }



class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['project_id', 'name', 'description', 'start_date', 'end_date', 'staff_id', 'completed']
        labels = {
            'project_id':'Select Project'
        }
        widgets = {
            'project_id': forms.Select(attrs={
                'class':'form-control form-control-user',
                'required': True
                }),
            'name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Job Name',
                'required': True
                }),
            'description': forms.Textarea(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Description',
                'rows':'2',
                }),
            'start_date': forms.DateInput(attrs={
                'class':'form-control form-control-user',
                'type':'date',
                }),
            'end_date': forms.DateInput(attrs={
                'class':'form-control form-control-user',
                'type':'date',
                }),
            'staff_id': forms.CheckboxSelectMultiple(attrs={ 
                'class':'form-check-input',
            }),
            'completed': forms.CheckboxInput(attrs={ 
                'class':'form-check-input',
            })
        }
        error_messages = {
            'project_id': {
                'required':'A project must be selected'
                },
            'name': {
                'required':'You must enter a project name'
                },
        }

    def clean(self):
        super(JobForm, self).clean()

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        completed = self.cleaned_data.get('completed')

        # if completed then dates are needed
        if completed and not start_date and not end_date:
            self._errors['The entered dates are invalid'] = self.error_class([
                'You need to enter start and end dates if the job is complete!'])

        # if end date entered and no start date throw error
        elif not start_date and end_date:
            self._errors['The entered dates are invalid'] = self.error_class([
                'You need to enter a start date if you have entered an end date'])
        
        # if start date is greater than end date
        if end_date and start_date:
            if end_date < start_date:
                self._errors['The entered dates are invalid'] = self.error_class([
                    'You have entered an end date that is before the start date'])

        # return the cleaned data
        return self.cleaned_data


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['job_id'].empty_label = None
        self.fields['job_id'].queryset = Job.objects.filter(completed=False).order_by('project_id')

    class Meta:
        model = Task
        fields = ['job_id', 'name', 'completed_date']
        labels = {
            'job_id':'Select Job',
            'name':'Create Task Name',
            'completed_date':'Completed Date'
        }
        widgets = {
            'job_id': forms.Select(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Job Id',
                'required': True
                }),
            'name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Task Name',
                'required': True
                }),
            'completed_date': forms.DateInput(attrs={
                'class':'form-control form-control-user',
                'type':'date'
                }),
        }
        error_messages = {
            'job_id':{
                'required': "Job ID is required"
            },
            'Name':{
                'required': "Task name is required"
            },
        }
    

class WorkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WorkForm, self).__init__(*args, **kwargs)
        self.fields['staff_id'].initial = self.user
        self.fields['job_id'].empty_label = None
        
        # If the user is an office user show all jobs, 
        # otherwise only show jobs allocated to that staff member
        if self.user.groups.filter(name='Office Staff').exists():
            self.fields['job_id'].queryset = Job.objects.all().order_by('project_id')
        else:
            self.fields['job_id'].queryset = Job.objects.filter(staff_id=self.user).order_by('project_id')

    class Meta:
        model = Work
        fields = ['staff_id', 'job_id', 'description', 'start_datetime', 'end_datetime']
        labels = {
            'staff_id':'Staff Member',
            'job_id':'Select Job'
        }
        widgets = {
            'staff_id': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Staff Id',
                'hidden': True
                }),
            'job_id': forms.Select(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Job Id',
                }),
            'description': forms.Textarea(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Description'
                }),
            'start_datetime': forms.DateTimeInput(attrs={
                'class':'form-control form-control-user',
                'type':'datetime-local'
                }),
            'end_datetime': forms.DateTimeInput(attrs={
                'class':'form-control form-control-user',
                'type':'datetime-local'
                }),
        }
        error_messages = {
            'description': {
                'required':'The Description field is required'
            },
            'start_datetime':{
                'required':'Start datetime is required'
            },
            'end_datetime':{
                'required':'End datetime is required'
            }
        }


    def clean(self):
        cleaned_data = super(WorkForm, self).clean()
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        
        # check start date is not greater than end date
        if start_datetime and end_datetime:
            if start_datetime > end_datetime:
                self.add_error('start_datetime', 'Start date cannot be greater than end date')
                self.add_error('end_datetime', 'End date cannot be less than end date')
        
        return cleaned_data


