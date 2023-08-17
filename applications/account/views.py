from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse

from applications.account.forms import LoginForm
from applications.reinventor.models import Company

from django.forms import model_to_dict

# Create your views here.

def userLogin(request):

    data = {
        'form': LoginForm,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['id'] = user.id

            objectCompany = (Company.objects.all()).first()
            if objectCompany:
                request.session['objectCompany'] = {
                    "co_name": objectCompany.co_name,
                    "co_address": objectCompany.co_address,
                    "co_latitude": objectCompany.co_latitude,
                    "co_longitude": objectCompany.co_longitude,
                }

            return redirect('reinventa_app:panel-control')
        else:
            data['error'] = 'Usuario o contraseña incorrectos.'
            messages.error(request, 'Usuario o contraseña incorrectos.')

            return render(request, 'administrator/login.html', data)
    else:
        return render(request, 'administrator/login.html', data)
    
def logout(request):
    logout(request)
    request.session.flush()
    response = redirect('account_app:login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

