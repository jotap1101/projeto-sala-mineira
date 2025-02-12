from django import forms
from .models import Employee
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

# Create your forms here.
class EmployeeLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(),
        error_messages={
            'required': 'Este campo é obrigatório.'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Este campo é obrigatório.'
        },
        label='Senha'
    )

    class Meta:
        model = Employee
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username or not Employee.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário não encontrado.')

        return username
    
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and Employee.objects.filter(username=username).exists():
            user = Employee.objects.get(username=username)

            if not user.check_password(password):
                raise forms.ValidationError('Senha incorreta.')

        return password

class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class EmployeeChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''