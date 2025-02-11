from django import forms
from django.forms import inlineformset_factory
from .models import Candidate, ContactInfo, Address, SocialNetwork

# Create your forms here.
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Digite o primeiro nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Digite o sobrenome'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'cpf': forms.TextInput(attrs={'placeholder': 'Digite o CPF'}),
            'rg': forms.TextInput(attrs={'placeholder': 'Digite o RG'}),
            'disability_description': forms.Textarea(attrs={'rows': 3, 'style': 'resize: none;', 'placeholder': 'Descreva a deficiência'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Selecione o gênero'
        self.fields['drivers_license_category'].empty_label = 'Selecione a categoria da CNH'

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Digite o número de telefone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite o email'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': 'Digite a rua'}),
            'number': forms.TextInput(attrs={'placeholder': 'Digite o número'}),
            'neighborhood': forms.TextInput(attrs={'placeholder': 'Digite o bairro'}),
            'complement': forms.TextInput(attrs={'placeholder': 'Digite o complemento'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Digite o CEP'}),
            'city': forms.Select(attrs={'placeholder': 'Selecione a cidade'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'Selecione a cidade'

class SocialNetworkForm(forms.ModelForm):
    class Meta:
        model = SocialNetwork
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Digite o nome da rede social'}),
            'url': forms.URLInput(attrs={'placeholder': 'Digite a URL da rede social'}),
        }

# Formsets para relações 1:N (create)
ContactInfoFormSet = inlineformset_factory(Candidate, ContactInfo, form=ContactInfoForm, extra=1, can_delete=False)
AddressFormSet = inlineformset_factory(Candidate, Address, form=AddressForm, extra=1, can_delete=False)
SocialNetworkFormSet = inlineformset_factory(Candidate, SocialNetwork, form=SocialNetworkForm, extra=1, can_delete=False)

# Formsets para relações 1:N (update)
ContactInfoUpdateFormSet = inlineformset_factory(Candidate, ContactInfo, form=ContactInfoForm, extra=0, can_delete=True)
AddressUpdateFormSet = inlineformset_factory(Candidate, Address, form=AddressForm, extra=0, can_delete=True)
SocialNetworkUpdateFormSet = inlineformset_factory(Candidate, SocialNetwork, form=SocialNetworkForm, extra=0, can_delete=True)