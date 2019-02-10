from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.box_list, name='movie_list'),
    url(r'^contact/', views.contact, name='contact'),
]