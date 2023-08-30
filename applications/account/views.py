from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from applications.account.forms import LoginForm
from applications.account.models import UserReinventor
from applications.reinventor.models import Company

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

            logo = ""
            try:
                objectUserReinventor = UserReinventor.objects.get(user=user)
                if objectUserReinventor.ur_typeuser == 1:
                    objectCompany = (Company.objects.all()).first()

                    if objectCompany:
                        logo = objectCompany.co_logo.url if objectCompany.co_logo else ""

                        request.session['objectCompany'] = {
                            "co_name": objectCompany.co_name,
                            "co_address": objectCompany.co_address,
                            "co_latitude": objectCompany.co_latitude,
                            "co_longitude": objectCompany.co_longitude,
                            "logo": logo,
                            "ur_typeuser": objectUserReinventor.ur_typeuser,
                        }
                    return redirect('reinventa_app:panel-control')
                else:
                    logo = objectUserReinventor.reinventor.re_logo.url if objectUserReinventor.reinventor.re_logo else ""
                    
                    request.session['objectCompany'] = {
                            "co_name": objectUserReinventor.reinventor.re_nameentity,
                            "co_address": objectUserReinventor.reinventor.re_address,
                            "co_latitude": objectUserReinventor.reinventor.re_latitude,
                            "co_longitude": objectUserReinventor.reinventor.re_longitude,
                            "logo": logo,
                            "ur_typeuser": objectUserReinventor.ur_typeuser,
                            "re_id": objectUserReinventor.reinventor.re_id,
                        }
                    return redirect('reinventa_app:list-request-reinventor')
            
            except:
                objectCompany = (Company.objects.all()).first()
                if objectCompany.co_logo:
                    logo = objectCompany.co_logo

                if objectCompany:
                    request.session['objectCompany'] = {
                        "co_name": objectCompany.co_name,
                        "co_address": objectCompany.co_address,
                        "co_latitude": objectCompany.co_latitude,
                        "co_longitude": objectCompany.co_longitude,
                        "logo": logo,
                        "ur_typeuser": 1,
                        "admin": True
                    }
                return redirect('reinventa_app:panel-control')

            
        else:
            data['error'] = 'Usuario o contraseña incorrectos.'
            messages.error(request, 'Usuario o contraseña incorrectos.')

            return render(request, 'administrator/login.html', data)
    else:
        return render(request, 'administrator/login.html', data)
    
def logout_view(request):
    logout(request)
    return redirect('account_app:login')

