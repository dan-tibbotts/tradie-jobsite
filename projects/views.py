from os import name
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from projects.models import *
from projects.forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.db.models import Q
from accounts.permissions import Permissions
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.decorators import login_required

''''Function Base View for searching'''

@login_required(login_url='login')
def search_result(request):
    project_context = {}
    job_context = {}
    task_context = {}
    work_context = {}
    staff_context = {}
    customer_context = {}
    print('im called')
    if request.method == 'GET':
        search_input = request.GET.get('search')
        # check projects
        try:
            project_context = Project.objects.distinct().filter(name__icontains=search_input)
        except:
            project_context = {}

        # check jobs
        try:
            job_context = Job.objects.distinct().filter(
                Q(name__icontains=search_input)|
                Q(staff_id__first_name__icontains=search_input)|
                Q(staff_id__last_name__icontains=search_input)|
                Q(project_id__name__icontains=search_input))
        except:
            job_context = {}
        
        # check tasks
        try:
            task_context = Task.objects.distinct().filter(
                Q(name__icontains=search_input)|
                Q(job_id__name__icontains=search_input)
                )
        except:
            task_context = {}

        # check works
        try:
            work_context = Work.objects.distinct().filter(
                Q(job_id__name__icontains=search_input)|
                Q(staff_id__first_name__icontains=search_input)|
                Q(staff_id__last_name__icontains=search_input))
        except:
            work_context = {}
        
        # checks customers
        try:
            customer_context = Customer.objects.distinct().filter(
                Q(company_name__icontains=search_input)|
                Q(first_name__icontains=search_input)|
                Q(last_name__icontains=search_input)|
                Q(phone__icontains=search_input)|
                Q(email__icontains=search_input)|
                Q(address_1__icontains=search_input)|
                Q(post_code__icontains=search_input)
            )
        except:
            customer_context = {}
        # checks staff
        try:
            staff_context = User.objects.distinct().filter(
                Q(first_name__icontains=search_input)|
                Q(last_name__icontains=search_input)|
                Q(email__icontains=search_input)|
                Q(username__icontains=search_input)
            )
        except:
            staff_context = {}
    return render(request, 'search-results.html', {'projects': project_context, 
        'jobs': job_context, 'works': work_context, 
        'tasks': task_context, 'customers':customer_context, 'staffs':staff_context})


''' CBVs for the app projects '''
#################
# Project Views #
#################

class CreateProject(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'project-new.html'
    form_class = ProjectForm
    success_url = reverse_lazy('job-new')

    # only office staff can create a project
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')


class EditProject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProjectForm
    template_name = 'project-edit.html'
    success_url = reverse_lazy('projects-all')
    model = Project

    # only office staff and supervisors can edit a project
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff', 'Supervisor')


class ViewProject(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project-view.html'
    context_object_name = "project"
    # all users can view a project


class ViewAllProjects(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects-all.html'
    context_object_name = 'projects'
    # all users can view all projects


class DeleteProject(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects-all')
    template_name = 'project-delete.html'

    # Only office staff can delete a project 
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')


#############
# Job Views #
#############

class CreateJob(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'job-new.html'
    form_class = JobForm
    success_url = reverse_lazy('task-new')

    # office staff or supervisor can create a job
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff', 'Supervisor')


class EditJob(LoginRequiredMixin, UpdateView):
    form_class = JobForm
    template_name = 'job-edit.html'
    model = Job
    success_url = reverse_lazy('jobs-all')

    # add test func to see if user is office staff, supervisor or is a trade staff assigned to the job
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff', 'Supervisor')



class JobDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'job-delete.html' 
    model = Job
    success_url = reverse_lazy('jobs-all')

    # office staff and supervisors can delete a job
    def test_func(self):    
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff', 'Supervisor')


class ViewJob(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'job-view.html'
    context_object_name = "job"
    # all users can view a job


class ViewAllJobs(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs-all.html'
    context_object_name = 'jobs'
    # all users can view all jobs


##############
# Task Views #
##############

class CreateTask(LoginRequiredMixin, CreateView):
    template_name = 'task-new.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks-all')
    # all users can create a task


class EditTask(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    template_name = 'task-edit.html'
    model = Task
    success_url = reverse_lazy('tasks-all')
    # all users can edit a task


class ViewTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task-view.html'
    context_object_name = "task"
    # all users can view a task


class ViewAllTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks-all.html'
    context_object_name = 'tasks'
    # all users can view all tasks


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks-all')
    template_name = 'task-delete.html'
    # all users can delete a task


##############
# Work Views #
##############

class CreateWork(LoginRequiredMixin, CreateView):
    template_name = 'work-new.html'
    form_class = WorkForm
    success_url = reverse_lazy('works-all')
    
    # all users can create their own works
    # current user initalised in WorkForm
    def get_form_kwargs(self):
        kwargs = super(CreateWork, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        images = self.request.FILES.getlist('images')
        self.object = form.save()
        
        # get all objects related to this image
        work_id = self.object
        job_id = self.object.job_id
        job = Job.objects.get(id = job_id.id)
        project = Project.objects.get(id=self.object.job_id.project_id.id)

        for image in images:
                photo = Image.objects.create(image=image, job_id=job, work_id=work_id, project_id=project)
                photo.save()
        return super().form_valid(form)


class EditWork(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = WorkForm
    template_name = 'work-edit.html'
    model = Work
    ccontext_object_name = 'work'
    success_url = reverse_lazy('works-all')

    # Sending user object to the form
    def get_form_kwargs(self):
        kwargs = super(EditWork, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    # office staff can edit work records, other users can edit their own record
    def test_func(self):
        user_field = self.get_object().staff_id  
        return Permissions(self.request).allow(user_field, 'Office Staff', '*Supervisor', '*Trade Staff')

    def form_valid(self, form):
        images = self.request.FILES.getlist('images')
        print(images)
        self.object = form.save()
        # get all objects related to this image
        work_id = self.object
        job_id = self.object.job_id
        job = Job.objects.get(id = job_id.id)
        project = Project.objects.get(id=self.object.job_id.project_id.id)

        for image in images:
            photo = Image.objects.create(image=image, job_id=job, work_id=work_id, project_id=project)
            photo.save()
                
        return super().form_valid(form)


class ViewWork(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Work
    template_name = 'work-view.html'
    context_object_name = "work"

    # office staff can view all work records, other users can view their own record
    def test_func(self):
        user_field = self.get_object().staff_id  
        return Permissions(self.request).allow(user_field, 'Office Staff', 'Supervisor', '*Trade Staff')


class ViewAllWorks(LoginRequiredMixin, ListView):
    model = Work
    template_name = 'works-all.html'
    context_object_name = "works"

    # Office staff can see all work records
    # Other users can only see their work records
    def get_queryset(self):
        if self.request.user.groups.filter(name='Office Staff').exists():
            return Work.objects.all()
        else:
            return Work.objects.filter(staff_id=self.request.user.id)


class DeleteWork(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Work
    success_url = reverse_lazy('works-all')
    template_name = 'work-delete.html'

    # only office staff can delete a work record
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')

class DeleteImage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    template_name = 'delete-image.html'
    context_object_name = 'image_object'

    def get_success_url(self):
        print(self.object)
        work_id = self.object.work_id.id
        return reverse_lazy('work-edit', kwargs={'pk': work_id})

    # only office staff can delete a work record
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')