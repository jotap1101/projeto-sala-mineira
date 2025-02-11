from django.db import models
from candidate.models import Candidate
from employee.models import Employee
import uuid

# Create your models here.
class AreaOfInterest(models.Model):
    class Meta:
        db_table = 'area_of_interest'
        verbose_name = 'Área de Interesse'
        verbose_name_plural = 'Áreas de Interesse'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class SubareaOfInterest(models.Model):
    class Meta:
        db_table = 'subarea_of_interest'
        verbose_name = 'Subárea de Interesse'
        verbose_name_plural = 'Subáreas de Interesse'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')
    area_of_interest = models.ForeignKey(AreaOfInterest, on_delete=models.PROTECT, verbose_name='Área de Interesse')

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    class Meta:
        db_table = 'skill'
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class StatusResume(models.Model):
    class Meta:
        db_table = 'status_resume'
        verbose_name = 'Status do Currículo'
        verbose_name_plural = 'Status dos Currículos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class Resume(models.Model):
    class Meta:
        db_table = 'resume'
        verbose_name = 'Currículo'
        verbose_name_plural = 'Currículos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='resume', verbose_name='Funcionário')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='resume', verbose_name='Candidato')
    summary = models.TextField(verbose_name='Resumo')
    subareas_of_interest = models.ManyToManyField(SubareaOfInterest, verbose_name='Subáreas de Interesse')
    skills = models.ManyToManyField(Skill, verbose_name='Habilidades')
    status = models.ForeignKey(StatusResume, on_delete=models.PROTECT, verbose_name='Status')
    is_deleted = models.BooleanField(default=False, verbose_name='Está deletado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return self.candidate.get_full_name()
    
class Institution(models.Model):
    class Meta:
        db_table = 'institution'
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class Course(models.Model):
    class Meta:
        db_table = 'course'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class Education(models.Model):
    class Meta:
        db_table = 'education'
        verbose_name = 'Educação'
        verbose_name_plural = 'Educações'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education', verbose_name='Currículo')
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, verbose_name='Instituição')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='Curso')
    start_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(null=True, blank=True, verbose_name='Data de Término')
    is_current = models.BooleanField(default=False, verbose_name='Está cursando atualmente')

    def __str__(self):
        return self.resume.candidate.get_full_name()
    
class Company(models.Model):
    class Meta:
        db_table = 'company'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class JobTitle(models.Model):
    class Meta:
        db_table = 'job_title'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class Experience(models.Model):
    class Meta:
        db_table = 'experience'
        verbose_name = 'Experiência'
        verbose_name_plural = 'Experiências'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience', verbose_name='Currículo')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Empresa')
    job_title = models.ForeignKey(JobTitle, on_delete=models.PROTECT, verbose_name='Cargo')
    start_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(null=True, blank=True, verbose_name='Data de Término')
    is_current = models.BooleanField(default=False, verbose_name='Está trabalhando atualmente')

    def __str__(self):
        return self.resume.candidate.get_full_name()
    
class Language(models.Model):
    class Meta:
        db_table = 'language'
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class LanguageProficiency(models.Model):
    class Meta:
        db_table = 'language_proficiency'
        verbose_name = 'Proficiência em Idioma'
        verbose_name_plural = 'Proficiências em Idiomas'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name
    
class ResumeLanguage(models.Model):
    class Meta:
        db_table = 'resume_language'
        verbose_name = 'Idioma do Currículo'
        verbose_name_plural = 'Idiomas dos Currículos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='language', verbose_name='Currículo')
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name='Idioma')
    language_proficiency = models.ForeignKey(LanguageProficiency, on_delete=models.PROTECT, verbose_name='Proficiência')

    def __str__(self):
        return self.resume.candidate.get_full_name()