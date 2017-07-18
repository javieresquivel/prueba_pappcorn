# -*- coding: utf-8 -*-
from django import forms
from banco.models import *
import json
from django.contrib.humanize.templatetags.humanize import intcomma

class BancoForm(forms.ModelForm):

   def clean_codigo(self):
      return self.cleaned_data.get("codigo").upper()

   class Meta:
      model = Banco
      exclude = ('usuario_registro','fecha_registro','estado_registro',)

class ClienteForm(forms.ModelForm):

   tipo_cuenta = forms.ChoiceField(choices=Cuenta.TIPOS_DE_CUENTAS)
   cuentas = forms.CharField(initial='[]',widget=forms.HiddenInput)

   def __init__(self, *args, **kwargs):
     self.banco = kwargs.pop("banco",None)
     super(ClienteForm, self).__init__(*args, **kwargs)

   def clean_cuentas(self):
      cuentas = json.loads(self.cleaned_data.get("cuentas") or "[]")
      info = []
      for c in cuentas:
         tipo_cuenta = int(c["tipo_cuenta"])
         cuenta = c["numero_cuenta"].upper()
         tarjeta = c["numero_tarjeta"].upper()

         existe = Cuenta.objects.filter(estado_registro=True,numero_cuenta=cuenta,tipo=tipo_cuenta,cliente__banco=self.banco)
         if existe:
            raise forms.ValidationError("La cuenta numero "+cuenta+" ya se encuentra registrada.")
         existe = TarjetaDebito.objects.filter(estado_registro=True,numero=tarjeta,cuenta__cliente__banco=self.banco)
         if existe:
            raise forms.ValidationError("La tarjeta numero "+tarjeta+" ya se encuentra registrada.")

         info.append({
            "cuenta": Cuenta(tipo=tipo_cuenta,numero_cuenta= cuenta),
            "tarjeta": TarjetaDebito(numero=tarjeta)
         })
      return info

   class Meta:
      model = Cliente
      exclude = ('usuario_registro','fecha_registro','estado_registro','banco')

class TransaccionForm(forms.ModelForm):

   def clean(self):
      cleaned_data = super(TransaccionForm,self).clean()
      if cleaned_data.get("tipo") == Transaccion.TRANSFERENCIA:
         if not cleaned_data.get("cuenta_destino"):
            raise forms.ValidationError("Debe ingresarse la cuenta destino de la transferencia")
         if cleaned_data.get("cuenta") == cleaned_data.get("cuenta_destino"):
            raise forms.ValidationError("No se puede realizar una transferencia entre la misma cuenta")
      else:
         cleaned_data["cuenta_destino"] = None

      if cleaned_data.get("valor") <=0:
         raise forms.ValidationError("El valor de la transacción debe ser mayor a 0")

      # Validar efectividad de transaccion
      if cleaned_data.get("tipo") == Transaccion.TRANSFERENCIA or cleaned_data.get("tipo") == Transaccion.RETIRO:
         saldo = cleaned_data.get("cuenta").get_saldo()
         if saldo < cleaned_data.get("valor"):
            raise forms.ValidationError("La cuenta "+unicode(cleaned_data.get("cuenta"))+" no tiene saldo suficiente. (Saldo: "+intcomma(saldo)+")")

      return cleaned_data
      

   class Meta:
      model = Transaccion
      exclude = ('usuario_registro','fecha_registro','estado_registro',)
    