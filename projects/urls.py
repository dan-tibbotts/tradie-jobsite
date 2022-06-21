from django.urls import path, include
from projects.views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('project/new/', CreateProject.as_view(), name='project-new'),
    path('project/<int:pk>', ViewProject.as_view(), name='project-view'),
    path('project/edit/<int:pk>', EditProject.as_view(), name='project-edit'),
    path('project/delete/<int:pk>', DeleteProject.as_view(), name='project-delete'),
    path('project/view-all/', ViewAllProjects.as_view(), name='projects-all'),

    path('job/new/', CreateJob.as_view(), name='job-new'),
    path('job/<str:pk>', ViewJob.as_view(), name='job-view'),
    path('job/edit/<str:pk>', EditJob.as_view(), name='job-edit'),
    path('job/delete/<str:pk>', JobDelete.as_view(), name='job-delete'),
    path('job/view-all/', ViewAllJobs.as_view(), name='jobs-all'),
    
    path('task/new/', CreateTask.as_view(), name='task-new'),
    path('task/<str:pk>', ViewTask.as_view(), name='task-view'),
    path('task/edit/<str:pk>', EditTask.as_view(), name='task-edit'),
    path('task/delete/<str:pk>', DeleteTask.as_view(), name='task-delete'),
    path('task/view-all/', ViewAllTasks.as_view(), name='tasks-all'),

    path('work/new/', CreateWork.as_view(), name='work-new'),
    path('work/<str:pk>', ViewWork.as_view(), name='work-view'),
    path('work/edit/<str:pk>', EditWork.as_view(), name='work-edit'),
    path('work/delete/<str:pk>', DeleteWork.as_view(), name='work-delete'),
    path('work/view-all/', ViewAllWorks.as_view(), name='works-all'),

    path('work/delete/image/<int:pk>', DeleteImage.as_view(), name='delete-image'),
    
    path('search/', search_result, name='search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
