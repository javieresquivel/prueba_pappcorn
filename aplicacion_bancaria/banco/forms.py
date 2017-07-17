from django import forms
from banco.models import *
import json

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
