from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def controlPanel(request):
    lst_bases = []

    data = {
        'lst_bases': lst_bases,
    }
    return render(request, 'reinventor/pages/maps.html', data)