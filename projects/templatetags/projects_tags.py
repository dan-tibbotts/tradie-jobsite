from django import template
from datetime import date, datetime, timedelta
from django.db.models import Sum
from projects.models import Project, Job, Task, Work, Image

register = template.Library()


# Project Tags #
@register.simple_tag
def get_all_projects():
    return Project.objects.all()

@register.simple_tag
def get_projects_by_customer(customer):
    return Project.objects.filter(customer_id=customer.id)

@register.simple_tag
def get_open_projects():
    return Project.objects.filter(status=0)

@register.simple_tag
def count_total_projects():
    return Project.objects.all().count()

@register.simple_tag
def count_open_projects():
    return Project.objects.filter(status=0).count()

@register.simple_tag
def count_on_hold_projects():
    return Project.objects.filter(status=1).count()

@register.simple_tag
def count_closed_projects():
    return Project.objects.filter(status=2).count()


# Job Tags #
@register.simple_tag
def get_all_user_jobs(user):
    return Job.objects.filter(staff_id=user.id)

@register.simple_tag
def get_all_jobs_by_customer(customer):
    return Job.objects.filter(project_id__customer_id=customer.id)

@register.simple_tag
def get_all_jobs_by_project(project):
    return Job.objects.filter(project_id=project.id)

@register.simple_tag
def get_all_jobs_by_user_and_project(user, project):
    return Job.objects.filter(staff_id=user.id, project_id=project.id)

@register.simple_tag
def count_total_jobs():
    return Job.objects.all().count()

@register.simple_tag
def count_user_jobs(user):
    return Job.objects.filter(staff_id=user.id).count()

@register.simple_tag
def count_uncompleted_jobs():
    return Job.objects.filter(completed=False).count()

@register.simple_tag
def count_completed_jobs():
    return Job.objects.filter(completed=True).count()

@register.simple_tag
def count_overdue_jobs():
    return Job.objects.filter(end_date__lt=date.today(), completed=False).count()


# Task Tags #
@register.simple_tag
def count_total_tasks():
    return Task.objects.all().count()

@register.simple_tag
def count_uncompleted_tasks():
    return Task.objects.filter(completed_date=None).count()

@register.simple_tag
def count_completed_tasks():
    return Task.objects.exclude(completed_date=None).count()


# Work Tags #
@register.simple_tag
def get_work_by_project(project):
    return Work.objects.filter(job_id__project_id=project.id)

@register.simple_tag
def get_work_by_job(job):
    return Work.objects.filter(job_id=job.id)

@register.simple_tag
def get_work_by_staff_member(staff):
    return Work.objects.filter(staff_id=staff.id).order_by('start_datetime')

@register.simple_tag
def get_total_work_hours_by_job(job):
    total = 0
    total_hours = 0
    try:
        work_records = Work.objects.filter(job_id=job.id)

        for work in work_records:
            total_time = work.end_datetime - work.start_datetime
            hours = total_time.seconds / 60 / 60
            total_hours += hours

        minutes = total_hours % 1
        minutes = 60 * minutes
        minutes = str(minutes)
        total = (str(total_hours)[0:2] + " " + " hrs" + " " + minutes[0:2] + " " + "mins")

        return total
    except: 
        return total
    
# Image Tags #
@register.simple_tag
def get_all_images():
    return Image.objects.all()

@register.simple_tag
def get_work_images(work):
    return Image.objects.filter(work_id=work.id)

@register.simple_tag
def count_work_images(work):
    return Image.objects.filter(work_id=work.id).count()

@register.simple_tag
def count_job_images(job):
    return Image.objects.filter(job_id=job.id).count()

@register.simple_tag
def count_project_images(project):
    return Image.objects.filter(project_id=project.id).count()

@register.simple_tag
def get_job_images(job):
    return Image.objects.filter(job_id=job.id)

@register.simple_tag
def get_project_images(project):
    return Image.objects.filter(project_id=project.id)