from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from applications.account.models import Comuna, Pais, Region, Reinventor, UserReinventor, WithdrawalRequestReinventor
from applications.reinventor.forms import CompanyForm, ReinventorForm, UserForm
from applications.reinventor.models import Company
from reinventa.utils import getLatitudeLongitude

# Create your views here.

@login_required
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
            frm.is_staff = True
            frm.is_superuser = True
            frm.set_password(request.POST['password'])
            frm.save()

            ur = UserReinventor()
            ur.user = frm
            

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
            password = object.username
            hashed_password = make_password(password)
            frm.password = hashed_password
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
    return render(request, 'administrator/pages/form_reinventor.html', data)


@login_required
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
    else:
        form = CompanyForm()
        acction = 'crear'
        co_id = False

    data = {
        'form': form,
        'acction': acction,
        'co_id': co_id
    }
    return render(request, 'administrator/pages/form_company.html', data)


@login_required
def addConfiguration(request):

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.pais = Pais.objects.get(pa_id = request.POST['pais'])
            frm.region = Region.objects.get(re_id = request.POST['region'])
            frm.comuna = Comuna.objects.get(com_id = request.POST['comuna'])
            frm.save()

            address = f"{ frm.co_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)
            
            frm.co_latitude = lat
            frm.co_longitude = lng
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
        form = CompanyForm(request.POST, instance=object)
        if form.is_valid():
            # Guardar los datos del formulario UserForm
            frm = form.save(commit=False)
            frm.pais = Pais.objects.get(pa_id = request.POST['pais'])
            frm.region = Region.objects.get(re_id = request.POST['region'])
            frm.comuna = Comuna.objects.get(com_id = request.POST['comuna'])
            frm.save()

            address = f"{ frm.co_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)
            
            frm.co_latitude = lat
            frm.co_longitude = lng
            frm.save()

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
    lst_bases = []

    data = {
        'lst_bases': lst_bases,
    }
    return render(request, 'administrator/pages/maps.html', data)


@login_required
def verReinventores(request):
    objectData = Reinventor.objects.filter(re_active = "Y")
    data = {
        'objectData': objectData,
    }
    return render(request, 'administrator/pages/ver_reinventores.html', data)


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
            frm.save()

            address = f"{ frm.re_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)
            
            frm.re_latitude = lat
            frm.re_longitude = lng
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
            frm.save()

            address = f"{ frm.re_address }, { frm.comuna.com_nombre }, { frm.region.re_nombre }, { frm.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)
            
            frm.re_latitude = lat
            frm.re_longitude = lng
            frm.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Reinventor editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = ReinventorForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        're_id': re_id,
    }
    return render(request, 'administrator/pages/form_reinventor.html', data)


@login_required
def deleteReinventor(request, re_id):
    object = get_object_or_404(Reinventor, re_id=re_id)
    object.re_active = 'N'
    object.save()
    return redirect('reinventa_app:ver-reinventores')