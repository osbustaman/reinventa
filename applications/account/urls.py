from django.urls import path
from . import views

app_name = 'account_app'

urlpatterns = [
    path('', views.userLogin, name='login'),
    path('cerrar-sesion/', views.logout, name='cerrar-sesion'),
]
