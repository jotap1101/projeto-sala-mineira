from candidate.forms import CandidateForm, ContactInfoFormSet, AddressFormSet, SocialNetworkFormSet, ContactInfoUpdateFormSet, AddressUpdateFormSet, SocialNetworkUpdateFormSet
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import localtime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame, ListFlowable, ListItem, FrameBreak
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT
from .forms import ResumeForm, EducationFormSet, ExperienceFormSet, ResumeLanguageFormSet, EducationUpdateFormSet, ExperienceUpdateFormSet, ResumeLanguageUpdateFormSet, ResumeFilterForm
from .models import Resume
import os

# Create your views here.
@login_required(login_url='employee:login')
def list_resumes(request):
    # resumes = Resume.objects.select_related('candidate').filter(is_deleted=False)
    resumes = Resume.objects.select_related('candidate').all()
    resume_filter_form = ResumeFilterForm()
    context = {
        'resumes': resumes,
        'resume_filter_form': resume_filter_form,
    }

    return render(request, 'resume/list_resumes.html', context)

@login_required(login_url='employee:login')
def create_resume(request):
    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST, request.FILES)
        resume_form = ResumeForm(request.POST)

        contact_info_formset = ContactInfoFormSet(request.POST)
        address_formset = AddressFormSet(request.POST)
        social_network_formset = SocialNetworkFormSet(request.POST)

        education_formset = EducationFormSet(request.POST)
        experience_formset = ExperienceFormSet(request.POST)
        resume_language_formset = ResumeLanguageFormSet(request.POST)

        if (candidate_form.is_valid() and resume_form.is_valid() and
            contact_info_formset.is_valid() and address_formset.is_valid() and social_network_formset.is_valid() and
            education_formset.is_valid() and experience_formset.is_valid() and resume_language_formset.is_valid()):

            with transaction.atomic():
                candidate = candidate_form.save()

                contact_info_formset.instance = candidate
                contact_info_formset.save()
                address_formset.instance = candidate
                address_formset.save()
                social_network_formset.instance = candidate
                social_network_formset.save()

                resume = resume_form.save(commit=False)
                resume.employee = request.user
                resume.candidate = candidate
                resume.save()

                resume_form.save_m2m()

                education_formset.instance = resume
                education_formset.save()
                experience_formset.instance = resume
                experience_formset.save()
                resume_language_formset.instance = resume
                resume_language_formset.save()

                messages.success(request, 'Currículo criado com sucesso.')

                return redirect('resume:list_resumes')

    else:
        candidate_form = CandidateForm()
        contact_info_formset = ContactInfoFormSet()
        address_formset = AddressFormSet()
        social_network_formset = SocialNetworkFormSet()

        resume_form = ResumeForm()
        education_formset = EducationFormSet()
        experience_formset = ExperienceFormSet()
        resume_language_formset = ResumeLanguageFormSet()

    context = {
        'candidate_form': candidate_form,
        'resume_form': resume_form,
        'contact_info_formset': contact_info_formset,
        'address_formset': address_formset,
        'social_network_formset': social_network_formset,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'resume_language_formset': resume_language_formset,
    }

    return render(request, 'resume/create_update_resume.html', context)

@login_required(login_url='employee:login')
def update_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    candidate = resume.candidate

    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST, request.FILES, instance=candidate)
        resume_form = ResumeForm(request.POST, instance=resume)

        contact_info_formset = ContactInfoUpdateFormSet(request.POST, instance=candidate)
        address_formset = AddressUpdateFormSet(request.POST, instance=candidate)
        social_network_formset = SocialNetworkUpdateFormSet(request.POST, instance=candidate)

        education_formset = EducationUpdateFormSet(request.POST, instance=resume)
        experience_formset = ExperienceUpdateFormSet(request.POST, instance=resume)
        resume_language_formset = ResumeLanguageUpdateFormSet(request.POST, instance=resume)

        if (candidate_form.is_valid() and resume_form.is_valid() and
            contact_info_formset.is_valid() and address_formset.is_valid() and social_network_formset.is_valid() and
            education_formset.is_valid() and experience_formset.is_valid() and resume_language_formset.is_valid()):
            
            if (candidate_form.has_changed() or resume_form.has_changed() or
            contact_info_formset.has_changed() or address_formset.has_changed() or social_network_formset.has_changed() or
            education_formset.has_changed() or experience_formset.has_changed() or resume_language_formset.has_changed()):
            
                with transaction.atomic():
                    candidate = candidate_form.save()

                    contact_info_formset.instance = candidate
                    contact_info_formset.save()
                    address_formset.instance = candidate
                    address_formset.save()
                    social_network_formset.instance = candidate
                    social_network_formset.save()

                    resume = resume_form.save(commit=False)
                    resume.candidate = candidate
                    resume.save()

                    resume_form.save_m2m()

                    education_formset.instance = resume
                    education_formset.save()
                    experience_formset.instance = resume
                    experience_formset.save()
                    resume_language_formset.instance = resume
                    resume_language_formset.save()

                    messages.success(request, 'Currículo atualizado com sucesso.')

                    return redirect('resume:list_resumes')
            else:
                messages.info(request, 'Nenhuma alteração foi feita.')

                return redirect('resume:list_resumes')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')

    else:
        candidate_form = CandidateForm(instance=candidate)
        contact_info_formset = ContactInfoUpdateFormSet(instance=candidate)
        address_formset = AddressUpdateFormSet(instance=candidate)
        social_network_formset = SocialNetworkUpdateFormSet(instance=candidate)

        resume_form = ResumeForm(instance=resume)
        education_formset = EducationUpdateFormSet(instance=resume)
        experience_formset = ExperienceUpdateFormSet(instance=resume)
        resume_language_formset = ResumeLanguageUpdateFormSet(instance=resume)

    context = {
        'candidate_form': candidate_form,
        'resume_form': resume_form,
        'contact_info_formset': contact_info_formset,
        'address_formset': address_formset,
        'social_network_formset': social_network_formset,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'resume_language_formset': resume_language_formset,
    }

    return render(request, 'resume/create_update_resume.html', context)

@login_required(login_url='employee:login')
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    
    if resume.is_deleted:
        messages.warning(request, 'Este currículo já foi excluído. Não é possível excluí-lo novamente.')
    else:
        resume.is_deleted = True
        resume.save()
        messages.success(request, 'Currículo excluído com sucesso.')

    return redirect('resume:list_resumes')

@login_required(login_url='employee:login')
def filter_resumes(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ResumeFilterForm(request.GET)
        resumes = Resume.objects.select_related('candidate').all()
        resumes_before_filtering = Resume.objects.all()

        if form.is_valid():
            if form.cleaned_data.get('full_name'):
                full_name = form.cleaned_data['full_name']
                resumes = resumes.filter(
                    candidate__first_name__icontains=full_name
                ) | resumes.filter(
                    candidate__last_name__icontains=full_name
                )

            if form.cleaned_data.get('date_of_birth'):
                resumes = resumes.filter(candidate__date_of_birth=form.cleaned_data['date_of_birth'])

            if form.cleaned_data.get('gender'):
                resumes = resumes.filter(candidate__gender=form.cleaned_data['gender'])

            if form.cleaned_data.get('cpf'):
                resumes = resumes.filter(candidate__cpf__icontains=form.cleaned_data['cpf'])

            if form.cleaned_data.get('rg'):
                resumes = resumes.filter(candidate__rg__icontains=form.cleaned_data['rg'])

            if form.cleaned_data.get('has_disability'):
                resumes = resumes.filter(candidate__has_disability=form.cleaned_data['has_disability'])

            if form.cleaned_data.get('has_drivers_license'):
                resumes = resumes.filter(candidate__has_drivers_license=form.cleaned_data['has_drivers_license'])

            if form.cleaned_data.get('is_first_job'):
                resumes = resumes.filter(candidate__is_first_job=form.cleaned_data['is_first_job'])

            if form.cleaned_data.get('is_currently_employed'):
                resumes = resumes.filter(candidate__is_currently_employed=form.cleaned_data['is_currently_employed'])

            if form.cleaned_data.get('employee'):
                resumes = resumes.filter(employee=form.cleaned_data['employee'])

            if form.cleaned_data.get('status'):
                resumes = resumes.filter(status=form.cleaned_data['status'])

            if form.cleaned_data.get('is_deleted'):
                resumes = resumes.filter(is_deleted=form.cleaned_data['is_deleted'])

            if form.cleaned_data.get('created_at'):
                created_at_date = form.cleaned_data['created_at']
                resumes = resumes.filter(created_at__date=created_at_date)

            if form.cleaned_data.get('updated_at'):
                updated_at_date = form.cleaned_data['updated_at']
                resumes = resumes.filter(updated_at__date=updated_at_date)

        data = {
            'count': resumes_before_filtering.count(),
            'resumes': [
                {
                    'id': resume.id,
                    'candidate': f'{resume.candidate.first_name} {resume.candidate.last_name}',
                    'created_at': localtime(resume.created_at).strftime('%d/%m/%Y às %H:%M'),
                    'updated_at': localtime(resume.updated_at).strftime('%d/%m/%Y às %H:%M'),
                }
                for resume in resumes
            ]
        }

        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Requisição inválida'}, status=400)

@login_required(login_url='employee:login')
def download_resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{resume.candidate.get_full_name()}.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    width, height = A4
    candidate = resume.candidate
    contact_info = candidate.contact_info.all()
    address = candidate.address.all()
    x_offset = 2 * cm
    y_offset = height - 2 * cm

    if candidate.photo:
        image_path = os.path.join(settings.MEDIA_ROOT, candidate.photo.name)
        image_reader = ImageReader(image_path)
        image_width, image_height = image_reader.getSize()
        aspect_ratio = image_height / image_width
        img_width = 4 * cm
        img_height = img_width * aspect_ratio

        if img_height > 4 * cm:
            img_height = 4 * cm
            img_width = img_height / aspect_ratio

        p.drawImage(image_path, x_offset, y_offset - img_height, width=img_width, height=img_height)
        x_offset += img_width + 1 * cm

    p.setFont('Helvetica-Bold', 17)
    p.drawString(x_offset, y_offset - 0.6 * cm, candidate.get_full_name())
    
    y_offset -= 0 * cm

    p.setFont('Helvetica', 11)

    p.drawString(x_offset, y_offset - 1.5 * cm, f'Data de Nascimento: {candidate.date_of_birth.strftime('%d/%m/%Y')}')
    p.drawString(x_offset, y_offset - 2 * cm, f'CNH: {'Sim - ' + candidate.drivers_license_category.name if candidate.has_drivers_license else 'Não'}')
    # formatted_cpf = f"{candidate.cpf[:3]}.{candidate.cpf[3:6]}.{candidate.cpf[6:9]}-{candidate.cpf[9:]}"
    # p.drawString(x_offset, y_offset - 2.5 * cm, f'CPF: {formatted_cpf}')
    
    y_offset -= 2.5 * cm

    p.drawString(x_offset, y_offset - 0.01 * cm, f'Endereço: {address[0].street}, {address[0].number} - {address[0].neighborhood} - {address[0].city}/{address[0].city.state.abbreviation}')

    y_offset -= 0.5 * cm

    formatted_phone_number = f"({contact_info[0].phone_number[:2]}) {contact_info[0].phone_number[2:7]}-{contact_info[0].phone_number[7:]}"
    p.drawString(x_offset, y_offset - 0.01 * cm, f'Telefone: {formatted_phone_number}')
    p.drawString(x_offset, y_offset - 0.5 * cm, f'Email: {contact_info[0].email}')

    y_offset -= 2 * cm
    styles = getSampleStyleSheet()
    elements = []

    styles = getSampleStyleSheet()

    if resume.summary:
        p.setFont('Helvetica-Bold', 12)
        p.drawString(2 * cm, y_offset, 'RESUMO')

        y_offset -= 0.2 * cm

        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)

        y_offset -= 0.3 * cm
        resume_paragraph = Paragraph(resume.summary, styles['Normal'])
        resume_width, resume_height = resume_paragraph.wrap(width - 4 * cm, height - y_offset)

        resume_paragraph.drawOn(p, 2 * cm, y_offset - resume_height)

        y_offset -= resume_height + 0.8 * cm


    if resume.education.exists():
        p.setFont('Helvetica-Bold', 12)
        p.drawString(2 * cm, y_offset, 'FORMAÇÃO ACADÊMICA')

        y_offset -= 0.2 * cm

        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)

        y_offset -= 0.8 * cm

        p.setFont('Helvetica', 11)

        for education in resume.education.all():
            # Nome do curso e instituição
            education_text_line1 = f'\u2022 {education.course.name} - {education.institution.name}'
            p.drawString(2 * cm, y_offset, education_text_line1)
            y_offset -= 0.5 * cm

            # Datas de início e término
            start_date = education.start_date.strftime('%Y')
            end_date = education.end_date.strftime('%Y') if education.end_date else 'Em andamento'
            education_text_line2 = f'   Início: {start_date} - Previsão de término: {end_date}'
            p.drawString(2 * cm, y_offset, education_text_line2)
            y_offset -= 0.5 * cm
            

        y_offset -= 0.5 * cm

    if resume.experience.exists():
        p.setFont('Helvetica-Bold', 12)
        p.drawString(2 * cm, y_offset, 'EXPERIÊNCIA PROFISSIONAL')

        y_offset -= 0.2 * cm

        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)

        y_offset -= 0.8 * cm

        p.setFont('Helvetica', 11)

        for experience in resume.experience.all():
            # Cargo
            job_title_text = f'\u2022 Cargo: {experience.job_title.name}'
            p.drawString(2 * cm, y_offset, job_title_text)
            y_offset -= 0.5 * cm

            # Empresa
            company_text = f'   Empresa: {experience.company.name}'
            p.drawString(2 * cm, y_offset, company_text)
            y_offset -= 0.5 * cm

            # Datas de início e término
            start_date = experience.start_date.strftime('%Y')
            end_date = experience.end_date.strftime('%Y') if experience.end_date else 'Em andamento'
            date_text = f'   Período: {start_date} -> {end_date}'
            p.drawString(2 * cm, y_offset, date_text)
            y_offset -= 0.8 * cm

        y_offset -= 0.5 * cm

    if resume.language.exists():
        p.setFont('Helvetica-Bold', 12)
        p.drawString(2 * cm, y_offset, 'IDIOMAS')

        y_offset -= 0.2 * cm

        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)

        y_offset -= 0.8 * cm

        p.setFont('Helvetica', 11)

        for language in resume.language.all():
            language_text = f'\u2022 {language.language.name} - {language.language_proficiency}'

            p.drawString(2 * cm, y_offset, language_text)

            y_offset -= 0.5 * cm

        y_offset -= 0.5 * cm

    p.showPage()
    p.save()

    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
