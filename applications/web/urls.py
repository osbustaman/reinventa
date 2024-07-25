from django.urls import path

from applications.web import views

app_name = 'web_app'

urlpatterns = [
    path('', views.news, name='news'),
]