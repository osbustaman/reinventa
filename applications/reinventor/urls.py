from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

app_name = 'reinventa_app'

urlpatterns = [
    path('dashboard/', views.controlPanel, name='panel-control'),
    path('listado-reinventores/', views.verReinventores, name='ver-reinventores'),
    path('crear-reinventor/', views.addReinventor, name='add-reinventor'),
    path('editar-reinventor/<int:re_id>', views.editReinventor, name='edit-reinventor'),
    path('borrar-reinventor/<int:re_id>', views.deleteReinventor, name='delete-reinventor'),
    path('logo-reinventor/<int:re_id>', views.addLogoReinventor, name='logo-reinventor'),

    path('configuracion', views.configurationCompany, name='configuracion'),

    path('crear-configuracion/', views.addConfiguration, name='crear-configuracion'),
    path('edit-configuracion/<int:co_id>', views.editConfiguration, name='edit-configuracion'),


    path('ver-request/', views.viewRequestAdmin, name='ver-request'),
    path('ver-user/', views.viewUserAdmin, name='ver-user'),
    path('add-user/', views.addUserAdmin, name='add-user'),
    path('edit-user/<int:id>', views.editUserAdmin, name='edit-user'),


    path('add-user-reinventor/<int:re_id>', views.addUserReinventor, name='add-user-reinventor'),
    path('edit-user-reinventor/<int:re_id>/<int:id>', views.editUserReinventor, name='edit-user-reinventor'),
    path('delete-user-reinventor/<int:re_id>/<int:id>', views.deleteUserReinventor, name='delete-user-reinventor'),


    path('list-request-reinventor/', views.listRequestReinventor, name='list-request-reinventor'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
