from django import template
from accounts.models import Customer, User
from django.contrib.auth.models import Group
from django.db.models import Count

register = template.Library()

# Generic Tags
@register.simple_tag
def is_office_staff(user):
    return user.groups.filter(name='Office Staff').exists()

@register.simple_tag
def is_trade_staff(user):
    return user.groups.filter(name='Trade Staff').exists()

@register.simple_tag
def is_only_trade_staff(user):
    trade = user.groups.filter(name='Trade Staff').exists()
    office = user.groups.filter(name='Office Staff').exists()
    supervisor = user.groups.filter(name='Supervisor').exists()
    return trade and not office and not supervisor

@register.simple_tag
def is_trade_staff(user):
    return user.groups.filter(name='Trade Staff').exists()

@register.simple_tag
def is_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()

# Customer Tags
@register.simple_tag
def count_all_customers():
    return Customer.objects.all().count()

# Staff Tags
@register.simple_tag
def count_all_staff():
    return User.objects.all().count()

@register.simple_tag
def get_staff_from_staff_username(username):
    return User.objects.get(username=username)

@register.simple_tag
def count_all_trade_staff():
    return User.objects.filter(groups__in=Group.objects.filter(name='Tradesmen')).count()

@register.simple_tag
def count_all_supervisor_staff():
    return User.objects.filter(groups__in=Group.objects.filter(name='Supervisor')).count()

@register.simple_tag
def count_all_office_staff():
    return User.objects.filter(groups__in=Group.objects.filter(name='Office Staff')).count()

@register.simple_tag
def check_login_attempt_error(form_errors):
    attempts = False
    for error in form_errors:
        if error == 'Too Many Login Attempts!':
            attempts = True
            break
    return attempts