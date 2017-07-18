from django.conf.urls import url
from banco.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^bancos/$', login_required(InicioView.as_view()), name="bancos"),
	url(r'^bancos/clientes/$', login_required(ClientesView.as_view()), name="clientes"),
	url(r'^bancos/transacciones/$', login_required(TransaccionesView.as_view()), name="transacciones"),
]
