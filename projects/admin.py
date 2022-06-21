from django.contrib import admin
from projects.models import *

admin.site.register(Project)
admin.site.register(Job)
admin.site.register(Task)
admin.site.register(Work)
admin.site.register(Image)