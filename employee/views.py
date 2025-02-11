from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmployeeLoginForm, EmployeeCreationForm, EmployeeChangeForm
from .models import Employee

# Create your views here.
def login_view(request):
    if not request.user.is_authenticated and 'next' in request.GET:
        messages.error(request, 'Você precisa estar logado para acessar a página solicitada. Faça login para continuar.')

    if request.method == 'POST':
        employee_login_form = EmployeeLoginForm(data=request.POST)

        if Employee.objects.filter(username=request.POST['username']).exists() and not Employee.objects.get(username=request.POST['username']).is_active:
            messages.error(request, 'Esta conta está inativa.')

            return redirect('employee:login')

        if employee_login_form.is_valid():
            user = authenticate(
                request,
                username=employee_login_form.cleaned_data['username'],
                password=employee_login_form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso.')

                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                else:
                    return redirect('employee:account')
        
        else:
            messages.error(request, 'Erro ao fazer login. Verifique os campos.')
            request.session['form_data'] = request.POST

        return redirect('employee:login')

    else:
        form_data = request.session.pop('form_data', None)
        employee_login_form = EmployeeLoginForm(data=form_data) if form_data else EmployeeLoginForm()

    context = {
        'employee_login_form': employee_login_form
    }

    return render(request, 'employee/login.html', context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout efetuado com sucesso.')

    return redirect('employee:login')

def register_view(request):
    if request.method == 'POST':
        employee_creation_form = EmployeeCreationForm(request.POST)

        if employee_creation_form.is_valid():
            employee_creation_form.save()
            messages.success(request, 'Cadastro efetuado com sucesso.')

            return redirect('employee:login')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os campos.')

            request.session['form_data'] = request.POST

            return redirect('employee:register')

    else:
        form_data = request.session.pop('form_data', None)
        employee_creation_form = EmployeeCreationForm(data=form_data) if form_data else EmployeeCreationForm()

    context = {
        'employee_creation_form': employee_creation_form
    }
    
    return render(request, 'employee/register.html', context)

@login_required(login_url='employee:login')
def account_view(request):
    context = {
        'employee': request.user,
        'employee_change_form': EmployeeChangeForm(instance=request.user)
    }

    return render(request, 'employee/account.html', context)

@login_required(login_url='employee:login')
def edit_account_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        employee_change_form = EmployeeChangeForm(request.POST, request.FILES, instance=employee)

        if employee_change_form.is_valid():
            employee_change_form.save()
            messages.success(request, 'Alterações salvas com sucesso.')

            return redirect('employee:account')
        else:
            messages.error(request, 'Erro ao salvar alterações. Verifique os campos.')

            request.session['form_data'] = request.POST

            return redirect('employee:edit_account', employee_id=employee_id)        
    else:
        form_data = request.session.pop('form_data', None)
        employee_change_form = EmployeeChangeForm(data=form_data, instance=employee) if form_data else EmployeeChangeForm(instance=employee)

    context = {
        'employee': request.user,
        'employee_change_form': employee_change_form
    }

    return render(request, 'employee/account.html', context)