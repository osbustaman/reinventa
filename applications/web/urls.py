from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from applications.web import views

app_name = 'web_app'

urlpatterns = [
    path('', views.news, name='news'),

]