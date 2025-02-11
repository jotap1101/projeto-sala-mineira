from django.contrib import admin
from .models import Gender, DriversLicenseCategory, Candidate, ContactInfo, State, City, Address, SocialNetwork

# Register your models here.
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    pass

@admin.register(DriversLicenseCategory)
class DriversLicenseCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    class ContactInfoInline(admin.StackedInline):
        model = ContactInfo
        extra = 1

    class AddressInline(admin.StackedInline):
        model = Address
        extra = 1

    class SocialNetworkInline(admin.StackedInline):
        model = SocialNetwork
        extra = 1

    inlines = [ContactInfoInline, AddressInline, SocialNetworkInline]

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    pass