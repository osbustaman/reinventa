from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse

from applications.account.forms import LoginForm

# Create your views here.

def login(request):

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

            #return HttpResponseRedirect(reverse('remun_app:panel'))
            return redirect('account_app:control_panel')
        else:
            data['error'] = 'Usuario o contraseña incorrectos.'
            messages.error(request, 'Usuario o contraseña incorrectos.')

            return render(request, 'reinventor/login.html', data)
    else:
        return render(request, 'reinventor/login.html', data)
    
def logout(request):
    logout(request)
    request.session.flush()
    response = redirect(reverse('account_base:login_client'))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

