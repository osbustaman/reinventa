from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from applications.reinventor.api.api import WithdrawalRequestUpdateAPIView, generatePdfAPIView
from applications.reinventor.views_error import error404
from . import views, views_ajax

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
    path('crear-request-reinventor/', views.addRequestReinventor, name='crear-request-reinventor'),
    path('edit-request-reinventor/<int:wrr_id>', views.editRequestReinventor, name='edit-request-reinventor'),
    path('ver-request-reinventor-adm/<int:wrr_id>', views.editRequestReinventor, name='edit-request-reinventor-adm'),


    path('add-observations/<int:wrr_id>', views.addObservations, name='add-observations'),
    path('edit-observations/<int:wrr_id>/<int:rt_id>', views.editObservations, name='edit-observations'),



    #ajax
    path('ajax/nueva-observacion/', views_ajax.new_observation, name='new_observation'),
    path('ajax/upload-file/', views_ajax.upload_file, name='upload_file'),
    path('ajax/download-excel-for-upload-reinventor/', views_ajax.download_excel_for_upload_reinventor, name='download_excel_for_upload_reinventor'),


    #api
    path('api/actualizar-estado/', WithdrawalRequestUpdateAPIView.as_view(), name='actualizar_estado'),
    path('api/generar-pdf/', generatePdfAPIView.as_view(), name='generar_pdf'),


    path('error404/', error404, name='error404'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
