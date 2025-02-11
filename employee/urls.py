from django.urls import path
from .views import login_view, logout_view, register_view, account_view, edit_account_view

app_name = 'employee'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('account/', account_view, name='account'),
    path('account/<uuid:employee_id>/edit/', edit_account_view, name='edit_account'),
]