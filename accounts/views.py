from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.http import request, response
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from accounts.models import *
from accounts.forms import *
from accounts.permissions import Permissions
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from BruteBuster.models import FailedAttempt


#################
# General Views #
#################

class LoginUser(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            user = request.POST['username']
            failed_user = FailedAttempt.objects.filter(username = user)[0]
            if failed_user.blocked():
                form.errors['Too Many Login Attempts!'] = ""
                form.add_error(None, "You have exceeded the total number of login attempts.")
            return self.form_invalid(form)


class LogoutUser(LogoutView):
    url = reverse_lazy('login')


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'
    # all users can view the dashboard


class ChangePassword(LoginRequiredMixin, UpdateView):
    template_name = 'password-change.html'
    model = User
    success_url = reverse_lazy('staff-view')
    fields = ['username', 'password1', 'password2']



##################
# Customer Views #
##################

class CreateCustomer(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'customer-new.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customers-all')
    
    # only office staff can create a customer
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')


class EditCustomer(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CustomerForm
    model = Customer
    template_name = 'customer-edit.html'
    success_url = reverse_lazy('customers-all')

    # only office staff and supervisors can edit a customer
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff', 'Supervisor')


class ViewCustomer(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customer-view.html'
    context_object_name = "customer"
    # all users can view a customer


class ViewAllCustomers(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers-all.html'
    context_object_name = 'customers'
    # all users can view all customers


class DeleteCustomer(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customers-all')
    template_name = 'customer-delete.html'

    # only office staff can delete a customer
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')


###############
# Staff Views #
###############

class CreateStaff(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'staff-new.html'
    form_class = StaffNewForm
    success_url = reverse_lazy('staff-all')
    context_object_name = "staff"

    def form_valid(self, form):
        # add staff to selected groups
        self.object = form.save()
        selected_groups = form.cleaned_data['groups']
        for selected_group in selected_groups:
            group = Group.objects.get(name=selected_group)
            group.user_set.add(self.object)
        return super().form_valid(form)

    # only office staff can create staff
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')


class EditStaff(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = StaffForm
    model = User
    template_name = 'staff-edit.html'
    context_object_name = 'staff'
    success_url = reverse_lazy('staff-all')

    def form_valid(self, form):
        self.object = form.save()
        selected_groups = form.cleaned_data['groups']
        for selected_group in selected_groups:
            group = Group.objects.get(name=selected_group)
            group.user_set.add(self.object)
        return super().form_valid(form)

    # office staff can edit all staff
    def test_func(self):
        user_field = self.get_object().username
        return Permissions(self.request).allow(user_field, 'Office Staff', '*Supervisor', '*Trade Staff')


class ViewStaff(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'staff-view.html'
    context_object_name = "staff"
    # all users can view staff


class ViewAllStaff(LoginRequiredMixin, ListView):
    model = User
    template_name = 'staff-all.html'
    context_object_name = 'staffs'
    # all users can view all staff


class DeleteStaff(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('staff-all')
    template_name = 'staff-delete.html'

    # only office staff can delete staff
    def test_func(self):
        user_field = None
        return Permissions(self.request).allow(user_field, 'Office Staff')

