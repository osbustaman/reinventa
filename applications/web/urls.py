from django.conf import settings
from django.conf.urls.static import static


from django.urls import path

from applications.web import views

app_name = 'web_app'

urlpatterns = [
    path('', views.news, name='news'),
    path('send-message', views.ajax_send_message, name='ajax_send_message'),
    path('to-subscribe', views.ajax_to_subscribe, name='ajax_to_subscribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)