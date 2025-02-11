from django.core.exceptions import ValidationError
from django.db import models
from .utils import generate_image_path
import os
import uuid

# Create your models here.
class Gender(models.Model):
    class Meta:
        db_table = 'gender'
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class DriversLicenseCategory(models.Model):
    class Meta:
        db_table = 'drivers_license_category'
        verbose_name = 'Categoria de CNH'
        verbose_name_plural = 'Categorias de CNH'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class Candidate(models.Model):
    class Meta:
        db_table = 'candidate'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    first_name = models.CharField(max_length=255, verbose_name='Nome')
    last_name = models.CharField(max_length=255, verbose_name='Sobrenome')
    date_of_birth = models.DateField(verbose_name='Data de Nascimento')
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, verbose_name='Gênero')
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF')
    rg = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name='RG')
    has_disability = models.BooleanField(default=False, verbose_name='Possui Deficiência')
    disability_description = models.TextField(null=True, blank=True, verbose_name='Descrição da Deficiência')
    has_drivers_license = models.BooleanField(default=False, verbose_name='Possui CNH')
    drivers_license_category = models.ForeignKey(DriversLicenseCategory, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Categoria da CNH')
    is_first_job = models.BooleanField(default=False, verbose_name='Primeiro Emprego')
    is_currently_employed = models.BooleanField(default=False, verbose_name='Atualmente Empregado')
    photo = models.ImageField(upload_to=generate_image_path, null=True, blank=True, verbose_name='Foto')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Candidate.objects.get(pk=self.pk)
                if old_instance.photo != self.photo:
                    if old_instance.photo and os.path.isfile(old_instance.photo.path):
                        os.remove(old_instance.photo.path)
            except Candidate.DoesNotExist:
                old_instance = None

        super(Candidate, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.exists(self.photo.path):
                try:
                    os.remove(self.photo.path)
                except Exception as e:
                    print(f'Error deleting file: {e}')

        super(Candidate, self).delete(*args, **kwargs)

    def clean(self):
        errors = {}

        if self.has_disability and not self.disability_description:
            errors['disability_description'] = 'Se o candidato possui deficiência, a descrição da deficiência é obrigatória'

        if not self.has_disability and self.disability_description:
            errors['has_disability'] = 'Se o candidato não possui deficiência, a descrição da deficiência não deve ser preenchida'

        if self.has_drivers_license and not self.drivers_license_category:
            errors['drivers_license_category'] = 'Se o candidato possui CNH, a categoria da CNH é obrigatória'

        if not self.has_drivers_license and self.drivers_license_category:
            errors['has_drivers_license'] = 'Se o candidato não possui CNH, a categoria da CNH não deve ser preenchida'

        if self.is_first_job and self.is_currently_employed:
            errors['is_currently_employed'] = 'Se o candidato está atualmente empregado, ele não pode ser considerado como primeiro emprego'
            errors['is_first_job'] = 'Se o candidato está atualmente empregado, ele não pode ser considerado como primeiro emprego'

        if errors:
            raise ValidationError(errors)


    def __str__(self):
        return self.get_full_name()
    
class ContactInfo(models.Model):
    class Meta:
        db_table = 'contact_info'
        verbose_name = 'Informação de Contato'
        verbose_name_plural = 'Informações de Contato'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='contact_info', verbose_name='Candidato')
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='Email')
    phone_number = models.CharField(max_length=11, verbose_name='Número de Telefone')

    def __str__(self):
        return self.candidate.get_full_name()
    
class State(models.Model):
    class Meta:
        db_table = 'state'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')
    abbreviation = models.CharField(max_length=2, unique=True, verbose_name='Sigla')

    def __str__(self):
        return self.name
    
class City(models.Model):
    class Meta:
        db_table = 'city'
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='Nome')
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name='Estado')

    def __str__(self):
        return self.name
    
class Address(models.Model):
    class Meta:
        db_table = 'address'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='address', verbose_name='Candidato')
    street = models.CharField(max_length=255, verbose_name='Rua')
    number = models.CharField(max_length=10, verbose_name='Número')
    neighborhood = models.CharField(max_length=255, verbose_name='Bairro')
    complement = models.CharField(max_length=255, null=True, blank=True, verbose_name='Complemento')
    zip_code = models.CharField(max_length=8, verbose_name='CEP')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Cidade')

    def __str__(self):
        return self.candidate.get_full_name()
    
class SocialNetwork(models.Model):
    class Meta:
        db_table = 'social_network'
        verbose_name = 'Rede Social'
        verbose_name_plural = 'Redes Sociais'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='social_network', verbose_name='Candidato')
    name = models.CharField(max_length=255, verbose_name='Nome')
    url = models.URLField(verbose_name='URL')

    def __str__(self):
        return self.candidate.get_full_name()