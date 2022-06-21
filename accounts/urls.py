from django.urls import path, include
from accounts.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', LoginUser.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name='password_reset_done'),
    
    path('password_change/<int:pk>', auth_views.PasswordChangeView.as_view(template_name='password_change.html', success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    path('dashboard/', Dashboard.as_view(), name='dashboard'),

    path('customer/new/', CreateCustomer.as_view(), name='customer-new'),
    path('customer/<str:pk>', ViewCustomer.as_view(), name='customer-view'),
    path('customer/edit/<str:pk>', EditCustomer.as_view(), name='customer-edit'),
    path('customer/delete/<str:pk>', DeleteCustomer.as_view(), name='customer-delete'),
    path('customer/view-all/', ViewAllCustomers.as_view(), name='customers-all'),
    

    path('staff/new/', CreateStaff.as_view(), name='staff-new'),
    path('staff/<int:pk>', ViewStaff.as_view(), name='staff-view'),
    path('staff/edit/<int:pk>', EditStaff.as_view(), name='staff-edit'),
    path('staff/delete/<str:pk>', DeleteStaff.as_view(), name='staff-delete'),
    path('staff/view-all/', ViewAllStaff.as_view(), name='staff-all'),
    

]

