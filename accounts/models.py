import uuid
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)

    company_name = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, default='New Zealand', null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_customer_name

    @property
    def get_customer_name(self):
        if self.company_name == None:
            return self.first_name + ' ' + self.last_name
        else:
            return self.company_name


