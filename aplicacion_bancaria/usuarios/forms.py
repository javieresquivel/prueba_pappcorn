# -*- coding: utf-8 -*-
from django import forms
from usuarios.models import Usuario

class FormIniciarSesion(forms.Form):
	usuario = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_usuario(self):
		try:
			usuario = Usuario.objects.get(username=self.cleaned_data.get('usuario'))
			if not usuario.is_active:
				raise forms.ValidationError("El usuario no se encuentra activo")
		except Exception as e:
			raise forms.ValidationError("El usuario ingresado no existe")
		return self.cleaned_data.get('usuario')

