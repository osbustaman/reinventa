from decouple import config

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from applications.account.models import Comuna, Pais, Region, Reinventor, RequestTracking, UserReinventor, WithdrawalRequestReinventor
from applications.reinventor.decorators import is_data
from applications.reinventor.forms import CompanyForm, ReinventorForm, ReinventorLogoForm, RequestTrackingForm, UserForm, WithdrawalRequestReinventorForm
from applications.reinventor.models import Company
from reinventa.Email import EmailSender
from reinventa.utils import getLatitudeLongitude

# Create your views here.

@login_required
@is_data
def viewRequestAdmin(request):
    objectsWithdrawalRequestReinventor = WithdrawalRequestReinventor.objects.filter(wrr_active = "Y")

    data = {
        'objectData': objectsWithdrawalRequestReinventor,
    }
    return render(request, 'administrator/pages/ver_request.html', data)


@login_required
def addUserAdmin(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.is_staff = False
            frm.is_superuser = False
            frm.set_password(request.POST['password'])
            frm.save()

            ur = UserReinventor()
            ur.user = frm
            ur.ur_typeuser = 1
            ur.save()

            messages.success(request, 'Usuario creado exitosamente!.')
            return redirect('reinventa_app:edit-user', id=frm.id)
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = UserForm()
    data = {
        'action': 'crear',
        'form': form
    }
    return render(request, 'administrator/pages/form_users.html', data)


@login_required
def editUserAdmin(request, id):
    object = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=object)
        if form.is_valid():
            frm = form.save(commit=False)

            if len(request.POST['password']) == 0:
                password = object.username
                hashed_password = make_password(password)
                frm.password = hashed_password
                frm.save()
            else:
                frm.set_password(request.POST['password'])
                frm.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Usuario editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = UserForm(instance=object)
    
    data = {
        'form': form,
        'action': 'editar',
        'id': id,
    }
    return render(request, 'administrator/pages/form_users.html', data)


@login_required
@is_data
def viewUserAdmin(request):
    objectsUserReinventor = UserReinventor.objects.filter(ur_active = "Y", ur_typeuser = 1)

    data = {
        'objectData': objectsUserReinventor,
    }
    return render(request, 'administrator/pages/ver_users.html', data)


@login_required
def configurationCompany(request):

    objCompany = (Company.objects.all()).first()

    if objCompany:
        form = CompanyForm(instance=objCompany)
        acction = 'editar'
        co_id = objCompany.co_id
        logo = objCompany.co_logo
        request.session['logo_company'] = logo.url
    else:
        form = CompanyForm()
        acction = 'crear'
        co_id = False
        logo = "../media/site/default_image.jpg"

    data = {
        'form': form,
        'acction': acction,
        'co_id': co_id,
        'logo': logo
    }
    return render(request, 'administrator/pages/form_company.html', data)


@login_required
def addConfiguration(request):

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.pais = Pais.objects.get(pa_id = request.POST['pais'])
            frm.region = Region.objects.get(re_id = request.POST['region'])
            frm.comuna = Comuna.objects.get(com_id = request.POST['comuna'])
            

            address = f"{ frm.co_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat_lng = getLatitudeLongitude(address)

            if not lat_lng:
                messages.error(request, "La ubicación no pudo ser detectada, ingrese la latitud y longitud manualmente")
                return redirect('reinventa_app:configuracion')

            frm.save()
            
            frm.co_latitude = lat_lng['latitude']
            frm.co_longitude = lat_lng['longitude']
            frm.save()

            messages.success(request, 'Configuración creada exitosamente!.')
            return redirect('reinventa_app:configuracion')
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return redirect('reinventa_app:configuracion')
    else:
        return redirect('reinventa_app:configuracion')

@login_required
def editConfiguration(request, co_id):
    object = get_object_or_404(Company, co_id=co_id)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=object)
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.pais = Pais.objects.get(pa_id = request.POST['pais'])
            frm.region = Region.objects.get(re_id = request.POST['region'])
            frm.comuna = Comuna.objects.get(com_id = request.POST['comuna'])
            frm.save()

            address = f"{ frm.co_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat_lng = getLatitudeLongitude(address)

            if not lat_lng:
                messages.error(request, "La ubicación no pudo ser detectada, ingrese la latitud y longitud manualmente")
                return redirect('reinventa_app:configuracion')
            
            frm.co_latitude = lat_lng['latitude']
            frm.co_longitude = lat_lng['longitude']
            frm.save()

            request.session['logo_company'] = f"media/{frm.co_logo.name}"

            # Agregar mensaje de éxito
            messages.success(request, 'Datos editados exitosamente!.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = CompanyForm(instance=object)

    return redirect('reinventa_app:configuracion')

@login_required
def controlPanel(request):
    
    excluded_results  = Reinventor.objects.filter(re_active='Y').filter(re_latitude__isnull=False, re_longitude__isnull=False)
    lstReinventrs = Reinventor.objects.filter(re_active='Y').exclude(re_latitude='').exclude(re_longitude='')

    try:
        objectCompany = Company.objects.all().first()
        request.session['lat_lng'] = {
            "co_latitude": objectCompany.co_latitude,
            "co_longitude": objectCompany.co_longitude,
        }
    except:
        pass

    data = {
        'lstReinventrs': lstReinventrs,
        'excluded_results': excluded_results,
        'cantReinventors': len(lstReinventrs)
    }
    return render(request, 'administrator/pages/maps.html', data)

@login_required
@is_data
def verReinventores(request):
    objectData = Reinventor.objects.filter(re_active = "Y")
    data = {
        'objectData': objectData,
    }
    return render(request, 'administrator/pages/ver_reinventores.html', data)

@login_required
def addUserReinventor(request, re_id):

    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.is_staff = False
            frm.is_superuser = False
            frm.set_password(request.POST['password'])
            frm.save()

            ur = UserReinventor()
            ur.user = frm
            ur.ur_typeuser = 2
            ur.reinventor = Reinventor.objects.get(re_id = re_id)
            ur.save()

            messages.success(request, 'Usuario creado exitosamente!.')
            return redirect('reinventa_app:edit-user-reinventor', re_id=re_id, id=frm.id)
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = UserForm()
    data = {
        'action': 'crear',
        'form': form,
        're_id': re_id
    }
    return render(request, 'administrator/pages/form_user_reinventor.html', data)

@login_required
def editUserReinventor(request, re_id, id):
    object = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=object)
        if form.is_valid():
            frm = form.save(commit=False)

            if len(request.POST['password']) == 0:
                password = object.username
                hashed_password = make_password(password)
                frm.password = hashed_password
                frm.save()
            else:
                frm.set_password(request.POST['password'])
                frm.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Usuario editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = UserForm(instance=object)

    objectsReinventor = Reinventor.objects.get(re_id = re_id)

    data = {
        'form': form,
        'action': 'Editar',
        'id': id,
        're_id': re_id,
        're_nameentity': objectsReinventor.re_nameentity,
    }
    return render(request, 'administrator/pages/form_user_reinventor.html', data)

@login_required
def addReinventor(request):

    if request.method == 'POST':
        form = ReinventorForm(request.POST)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.pais = Pais.objects.get(pa_id = request.POST['pais'])
            frm.region = Region.objects.get(re_id = request.POST['region'])
            frm.comuna = Comuna.objects.get(com_id = request.POST['comuna'])
            
            address = f"{ frm.re_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat_lng = getLatitudeLongitude(address)

            if not lat_lng:
                frm.save()
                messages.error(request, "La ubicación no pudo ser detectada, ingrese la latitud y longitud manualmente")
                return redirect('reinventa_app:add-reinventor')
            
            frm.re_latitude = lat_lng['latitude']
            frm.re_longitude = lat_lng['longitude']
            frm.save()

            messages.success(request, 'Reinventor creado exitosamente!.')
            return redirect('reinventa_app:edit-reinventor', re_id=frm.re_id)
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = ReinventorForm()
    data = {
        'action': 'Crear',
        'form': form
    }
    return render(request, 'administrator/pages/form_reinventor.html', data)

@login_required
def editReinventor(request, re_id):
    object = get_object_or_404(Reinventor, re_id=re_id)

    if request.method == 'POST':
        form = ReinventorForm(request.POST, instance=object)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.pais = Pais.objects.get(pa_id = request.POST['pais'])
            frm.region = Region.objects.get(re_id = request.POST['region'])
            frm.comuna = Comuna.objects.get(com_id = request.POST['comuna'])
            
            address = f"{ frm.re_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat_lng = getLatitudeLongitude(address)

            if not lat_lng:
                frm.save()
                messages.error(request, "La ubicación no pudo ser detectada, ingrese la latitud y longitud manualmente")
                return redirect('reinventa_app:edit-reinventor', re_id=re_id)
        
            frm.re_latitude = lat_lng['latitude']
            frm.re_longitude = lat_lng['longitude']
            frm.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Reinventor editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = ReinventorForm(instance=object)

    if object.re_latitude=='' and object.re_longitude=='':
        messages.error(request, f"La ubicación no pudo ser detectada, ingrese la latitud y longitud manualmente")

    objectsUserReinventors = UserReinventor.objects.filter(ur_active = "Y", ur_typeuser = 2, reinventor__re_id = re_id)
    formLogo = ReinventorLogoForm(instance=object)
    logo = f"/media/{str(object.re_logo)}"
    data = {
        'form': form,
        'formLogo': formLogo,
        'action': 'Editar',
        're_id': re_id,
        'objectsUserReinventors': objectsUserReinventors,
        're_nameentity': object.re_nameentity,
        'logo': logo,
    }
    return render(request, 'administrator/pages/form_reinventor.html', data)

@login_required
def addLogoReinventor(request, re_id):

    object = get_object_or_404(Reinventor, re_id=re_id)

    if request.method == 'POST':
        form = ReinventorLogoForm(request.POST, request.FILES, instance=object)
        
        if form.is_valid():
            form.save()

            messages.success(request, 'Imagen cargada exitosamente!.')
            return redirect('reinventa_app:edit-reinventor', re_id=re_id)
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return redirect('reinventa_app:edit-reinventor', re_id=re_id)
    else:
        messages.error("Error al guardar")
        return redirect('reinventa_app:edit-reinventor', re_id=re_id)

@login_required
def deleteUserReinventor(request, re_id, id):
    object = get_object_or_404(UserReinventor, user__id=id)
    object.ur_active = 'N'
    object.save()
    return redirect('reinventa_app:edit-reinventor', re_id=re_id)

@login_required
def deleteReinventor(request, re_id):
    object = get_object_or_404(Reinventor, re_id=re_id)
    object.re_active = 'N'
    object.save()
    return redirect('reinventa_app:ver-reinventores')

@login_required
def listRequestReinventor(request):
    reinventor = Reinventor.objects.get(re_id=request.session['objectCompany']['re_id'])
    objectsWithdrawalRequestReinventor = WithdrawalRequestReinventor.objects.filter(reinventor=reinventor)
    data = {
        'objects': objectsWithdrawalRequestReinventor,
    }
    return render(request, 'reinventor/pages/list_request_reinventor.html', data)

@login_required
def addRequestReinventor(request):
    if request.method == 'POST':
        form = WithdrawalRequestReinventorForm(request.POST)
        
        if form.is_valid():

            user_object = User.objects.get(id = request.session['id'])


            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.user = user_object
            frm.reinventor = Reinventor.objects.get(re_id=request.session['objectCompany']['re_id'])
            frm.wrr_estaterequest = 1
            frm.save()

            email_client = frm.user.email
            asunto = "Solicitud de retiro de residuos"
            html = f"<p>Estimado {frm.user.first_name} {frm.user.last_name},</p><p>Se ha creado una solicitud de retiro de residuos con el número {frm.wrr_id}.</p><p>Para ver el estado de la solicitud, ingrese a su panel de control.</p><p>Atentamente,</p><p>Equipo de {frm.reinventor.re_nameentity}</p>"

            rt = RequestTracking()
            rt.user = frm.user
            rt.withdrawalRequestReinventor = frm
            rt.rt_estaterequest = f"{ frm.wrr_estaterequest }"
            rt.rt_observation = "se envia correo de solicitud"
            rt.save()

                    # Crear una instancia de EmailSender
            email_sender = EmailSender(
                    config("MAIL_HOST")
                    , config("MAIL_PORT")
                    , config("MAIL_SECURE")
                    , config("MAIL_USER")
                    , config("MAIL_PASSWORD")
                    , config("MAIL_FROMNAME")
                    , config("MAIL_BBC")
            )

            send_email = email_sender.send_email(email_client, asunto, html, True)

            messages.success(request, 'Solicitud creada exitosamente!.')
            return redirect('reinventa_app:edit-request-reinventor', wrr_id=frm.wrr_id)
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = WithdrawalRequestReinventorForm()

    if 'ver-request-reinventor-adm/' in request.path:
        linkBack = reverse('reinventa_app:ver-request')
        viewEstaterequest = True
    else:
        linkBack = reverse('reinventa_app:list-request-reinventor')
        viewEstaterequest = False
    
    data = {
        'action': 'Crear',
        'form': form,
        'linkBack': linkBack,
        'viewEstaterequest': viewEstaterequest
    }
    return render(request, 'reinventor/pages/request.html', data)

@login_required
def editRequestReinventor(request, wrr_id):
    if 'ver-request-reinventor-adm/' in request.path:
        linkBack = reverse('reinventa_app:ver-request')
        viewEstaterequest = True
    else:
        linkBack = reverse('reinventa_app:list-request-reinventor')
        viewEstaterequest = False

    object = get_object_or_404(WithdrawalRequestReinventor, wrr_id=wrr_id)
    form = WithdrawalRequestReinventorForm(instance=object)

    objectsObservations = RequestTracking.objects.filter(withdrawalRequestReinventor=object)

    data = {
        'action': 'Editar',
        'form': form,
        'linkBack': linkBack,
        'viewEstaterequest': viewEstaterequest,
        'wrr_id': wrr_id,
        'objectsObservations': objectsObservations
    }
    return render(request, 'reinventor/pages/request.html', data)

@login_required
def addObservations(request, wrr_id):

    if request.method == 'POST':
        form = RequestTrackingForm(request.POST)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.user = User.objects.get(id = request.session['id'])
            frm.withdrawalRequestReinventor = WithdrawalRequestReinventor.objects.get(wrr_id=wrr_id)
            frm.save()

            messages.success(request, 'Observación creada exitosamente!.')
            return redirect('reinventa_app:edit-observations', wrr_id=wrr_id, rt_id=frm.rt_id)
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = RequestTrackingForm()
    data = {
        'action': 'Crear',
        'form': form,
        'wrr_id': wrr_id
    }
    return render(request, 'administrator/pages/form_observation.html', data)

@login_required
def editObservations(request, wrr_id, rt_id):
    object = get_object_or_404(RequestTracking, rt_id=rt_id)

    if request.method == 'POST':
        form = RequestTrackingForm(request.POST, instance=object)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.save()

            messages.success(request, 'Observación editada exitosamente!.')
        
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = RequestTrackingForm(instance=object)
    
    data = {
        'form': form,
        'action': 'Editar',
        'id': id,
        'wrr_id': wrr_id,
        'rt_id': rt_id
    }
    return render(request, 'administrator/pages/form_observation.html', data)



