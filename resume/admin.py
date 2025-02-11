from django.contrib import admin
from .models import AreaOfInterest, SubareaOfInterest, Skill, StatusResume, Resume, Institution, Course, Experience, Education, Company, JobTitle, Experience, Language, LanguageProficiency, ResumeLanguage

# Register your models here.
@admin.register(AreaOfInterest)
class AreaOfInterestAdmin(admin.ModelAdmin):
    pass

@admin.register(SubareaOfInterest)
class SubareaOfInterestAdmin(admin.ModelAdmin):
    pass

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass

@admin.register(StatusResume)
class StatusResumeAdmin(admin.ModelAdmin):
    pass

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    class EducationInline(admin.StackedInline):
        model = Education
        extra = 0

    class ExperienceInline(admin.StackedInline):
        model = Experience
        extra = 0

    class ResumeLanguageInline(admin.StackedInline):
        model = ResumeLanguage
        extra = 0

    inlines = [EducationInline, ExperienceInline, ResumeLanguageInline]
    filter_horizontal = ['skills', 'subareas_of_interest']
    list_display = ['id', 'is_deleted']
    list_editable = ['is_deleted']

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    pass

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(LanguageProficiency)
class LanguageProficiencyAdmin(admin.ModelAdmin):
    pass

@admin.register(ResumeLanguage)
class ResumeLanguageAdmin(admin.ModelAdmin):
    pass