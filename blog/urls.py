from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.box_list, name='movie_list'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^recommand/',views.reco, name='reco'),
    url(r'^reset/',views.reset_data, name='reset'),
]