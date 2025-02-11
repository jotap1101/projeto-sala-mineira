from candidate.models import *
from django import forms
from django.forms import inlineformset_factory
from resume.models import *

# Create your forms here.
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'
        exclude = ['employee', 'candidate']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3, 'style': 'resize: none;'}),
            'subareas_of_interest': forms.SelectMultiple(attrs={'placeholder': 'Selecione as áreas de interesse'}),
            'skills': forms.SelectMultiple(attrs={'placeholder': 'Selecione as habilidades'}),
        }

class ResumeFilterForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=False, label='Nome Completo')
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Nascimento')
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=False, label='Gênero')
    cpf = forms.CharField(max_length=11, required=False, label='CPF')
    rg = forms.CharField(max_length=10, required=False, label='RG')
    has_disability = forms.BooleanField(required=False, label='Possui Deficiência?')
    has_drivers_license = forms.BooleanField(required=False, label='Possui CNH?')
    is_first_job = forms.BooleanField(required=False, label='Primeiro Emprego?')
    is_currently_employed = forms.BooleanField(required=False, label='Atualmente Empregado?')
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, label='Funcionário')
    status = forms.ModelChoiceField(queryset=StatusResume.objects.all(), required=False, label='Status')
    is_deleted = forms.BooleanField(required=False, label='Está Deletado?')
    created_at = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Criação do Currículo')
    updated_at = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Atual. do Currículo')

# Formsets para relações 1:N (create)
EducationFormSet = inlineformset_factory(Resume, Education, fields='__all__', extra=1, can_delete=False)
ExperienceFormSet = inlineformset_factory(Resume, Experience, fields='__all__', extra=1, can_delete=False)
ResumeLanguageFormSet = inlineformset_factory(Resume, ResumeLanguage, fields='__all__', extra=1, can_delete=False)

# Formsets para relações 1:N (update)
EducationUpdateFormSet = inlineformset_factory(Resume, Education, fields='__all__', extra=0, can_delete=True)
ExperienceUpdateFormSet = inlineformset_factory(Resume, Experience, fields='__all__', extra=0, can_delete=True)
ResumeLanguageUpdateFormSet = inlineformset_factory(Resume, ResumeLanguage, fields='__all__', extra=0, can_delete=True)