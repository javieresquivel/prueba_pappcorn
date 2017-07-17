# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

class Autenticacion(View):
	TEMPLATE_LOGIN = 'login.html'

	def get(self,request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/bancos/')
		formulario = FormIniciarSesion()
		return render(request, self.TEMPLATE_LOGIN, locals())

	def post(self,request):
		formulario = FormIniciarSesion(request.POST)
		if formulario.is_valid():
			user = authenticate(username=formulario.cleaned_data.get('usuario'), password=formulario.cleaned_data.get('password'))
			if user:
				login(request,user)
				if 'next' in request.GET:
					return HttpResponseRedirect(request.GET['next'])
				else:
					return HttpResponseRedirect('/bancos/')
			mensaje_error = 'Clave incorrecta'
		return render(request, self.TEMPLATE_LOGIN, locals())

class CerrarSesion(View):

	def get(self,request):
		logout(request)
		return HttpResponseRedirect("/login")
