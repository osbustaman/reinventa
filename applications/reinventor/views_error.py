from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


@login_required
def error404(request):
    data = {
        'message': 'Debe configurar la empresa para poder acceder a este módulo. Pra hacer eso deb ir a Reinventa > Configuración y luego completar el formulario.'
    }
    return render(request, 'reinventor/pages/error404.html', data)