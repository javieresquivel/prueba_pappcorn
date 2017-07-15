from django.conf.urls import url
from usuarios.views import *

urlpatterns = [
	url(r'^$', Autenticacion.as_view(), name="login"),
	url(r'^logout/$', CerrarSesion.as_view(), name="logout"),
]
