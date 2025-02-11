from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class Employee(AbstractUser):
    class Meta:
        db_table = 'employee'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name='Email')
    profile_image = models.ImageField(upload_to='employee/profile_images', blank=True, null=True, verbose_name='Imagem de Perfil')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return self.get_full_name()