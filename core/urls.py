from django.urls import path
from django.shortcuts import redirect
from .views import home_view

app_name = 'core'

urlpatterns = [
    path('', lambda request: redirect('home/')),
    path('home/', home_view, name='home'),
]