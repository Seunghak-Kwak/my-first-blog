from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^finder/', views.finder, name='finder'),
]