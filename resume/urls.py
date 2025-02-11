from django.urls import path
from .views import *

app_name = 'resume'

urlpatterns = [
    path('list/', list_resumes, name='list_resumes'),
    path('create/', create_resume, name='create_resume'),
    # path('<uuid:resume_id>/detail;', resume_details, name='resume_details'),
    path('<uuid:resume_id>/update/', update_resume, name='update_resume'),
    path('<uuid:resume_id>/delete/', delete_resume, name='delete_resume'),
    path('filter/', filter_resumes, name='filter_resumes'),
    path('<uuid:resume_id>/pdf/', download_resume_pdf, name='download_pdf'),
]