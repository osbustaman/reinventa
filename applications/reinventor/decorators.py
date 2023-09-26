# -*- encoding: utf-8 -*-
from django.shortcuts import redirect
from applications.reinventor.models import Company

def is_data(func):
    def valida(request, *args, **kwargs):
        cantCompany = Company.objects.all().exists()
        if not cantCompany:
            valor = redirect('reinventa_app:error404')
        else:
            valor = func(request, *args, **kwargs)
        return valor

    return valida