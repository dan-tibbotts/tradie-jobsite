import uuid
from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.fields import related
from accounts.models import Customer

# Project Status
PROJECT_STATUS = (
    ('0' , 'Open',),
    ('1' , 'On Hold',),
    ('2' , 'Closed',),
)

class Project(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_projects")
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PROJECT_STATUS, default='0')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_project_id + ' - ' + self.name + " (" + self.customer_id.get_customer_name + ")"

    @property
    def get_project_id(self):
        return 'P' + str(self.id).zfill(5)


class Job(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_jobs")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    staff_id = models.ManyToManyField(User, related_name='user_jobs', blank=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_id.get_project_id + ' - ' + self.name + " (" + self.project_id.customer_id.get_customer_name + ")"

    @property
    def is_overdue(self):
        if self.end_date == None:
            return False
        else:
            return self.end_date < date.today()


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_tasks")
    name = models.CharField(max_length=50)
    completed_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_works')
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_works")
    description = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    @property 
    def get_total_time(self):
        return self.end_datetime - self.start_datetime


class Image(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    work_id = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="image_work", null=True, blank=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="image_job", null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add =True)
