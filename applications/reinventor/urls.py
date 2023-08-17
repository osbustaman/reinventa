from django.urls import path
from . import views

app_name = 'reinventa_app'

urlpatterns = [
    path('dashboard/', views.controlPanel, name='panel-control'),
    path('listado-reinventores/', views.verReinventores, name='ver-reinventores'),
    path('crear-reinventor/', views.addReinventor, name='add-reinventor'),
    path('editar-reinventor/<int:re_id>', views.editReinventor, name='edit-reinventor'),
    path('borrar-reinventor/<int:re_id>', views.deleteReinventor, name='delete-reinventor'),

    path('configuracion', views.configurationCompany, name='configuracion'),

    path('crear-configuracion/', views.addConfiguration, name='crear-configuracion'),
    path('edit-configuracion/<int:co_id>', views.editConfiguration, name='edit-configuracion'),


    path('ver-request/', views.viewRequestAdmin, name='ver-request'),
    path('ver-user/', views.viewUserAdmin, name='ver-user'),

]
