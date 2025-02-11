from django import forms
from django.forms import inlineformset_factory
from .models import Candidate, ContactInfo, Address, SocialNetwork

# Create your forms here.
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'disability_description': forms.Textarea(attrs={'rows': 3, 'style': 'resize: none;'}),
        }

# Formsets para relações 1:N (create)
ContactInfoFormSet = inlineformset_factory(Candidate, ContactInfo, fields='__all__', extra=1, can_delete=False)
AddressFormSet = inlineformset_factory(Candidate, Address, fields='__all__', extra=1, can_delete=False)
SocialNetworkFormSet = inlineformset_factory(Candidate, SocialNetwork, fields='__all__', extra=1, can_delete=False)

# Formsets para relações 1:N (update)
ContactInfoUpdateFormSet = inlineformset_factory(Candidate, ContactInfo, fields='__all__', extra=0, can_delete=True)
AddressUpdateFormSet = inlineformset_factory(Candidate, Address, fields='__all__', extra=0, can_delete=True)
SocialNetworkUpdateFormSet = inlineformset_factory(Candidate, SocialNetwork, fields='__all__', extra=0, can_delete=True)