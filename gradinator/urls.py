# urls that start with gradinator will be handled here
from django.conf.urls import url
from gradinator import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
