from django.urls import path
from . import views

app_name = 'reinventa_app'

urlpatterns = [
    path('dashboard/', views.controlPanel, name='panel-control'),
]
