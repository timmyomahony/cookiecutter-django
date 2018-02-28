from django.conf.urls import url

from core import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
