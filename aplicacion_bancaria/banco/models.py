# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from usuarios.models import Usuario
from django.db.models import Sum
import json

class ModeloBase(models.Model):

   fecha_registro = models.DateTimeField(auto_now_add=True)
   usuario_registro = models.ForeignKey(Usuario)
   estado_registro = models.BooleanField(default=True)
   observaciones = models.TextField(null=True,blank=True)

   class Meta:
      abstract = True

class Banco(ModeloBase):
   codigo = models.CharField(max_length=4,unique=True)
   nombre = models.CharField(max_length=250)
   direccion = models.CharField(max_length=250)

   def to_json(self):
      return {
         "id":self.id,
         "codigo":self.codigo,
         "nombre":self.nombre,
         "direccion":self.direccion,
         "usuario":unicode(self.usuario_registro),
         "fecha_registro":self.fecha_registro.strftime("%Y-%m-%d")
      }

   def get_clientes(self):
      return self.cliente_set.filter(estado_registro=True)

   def __unicode__(self):
      return unicode(self.codigo)+" - "+unicode(self.nombre)

class Cliente(ModeloBase):
   documento = models.CharField(max_length=50,unique=True)
   nombre = models.CharField(max_length=250)
   direccion = models.CharField(max_length=250)
   fecha_nacimiento = models.DateField()
   banco = models.ForeignKey(Banco)

   def get_cuentas(self):
      return self.cuenta_set.filter(estado_registro=True)

   def get_historial_transacciones(self):
      directas = Transaccion.objects.filter(cuenta__cliente=self)
      ids_directas = directas.values_list("id",flat=True)
      directas = list(directas)
      indirectas = list(Transaccion.objects.filter(cuenta_destino__cliente=self).exclude(pk__in=ids_directas))
      directas.extend(indirectas)
      return directas

   def get_json_cuentas(self):
      info = []
      cuentas = self.cuenta_set.filter(estado_registro=True)
      for c in cuentas:
         info.append({
            "id":c.id,
            "nombre_tipo_cuenta":c.get_tipo_display(),
            "numero_cuenta":c.numero_cuenta,
            "numero_tarjeta":c.get_tarjeta_debito().numero,
            "tipo_cuenta":c.tipo
         })
      return json.dumps(info)

   def __unicode__(self):
      return unicode(self.nombre)

class Cuenta(ModeloBase):
   AHORROS = 1
   CORRIENTE = 2
   OTRA = 3

   TIPOS_DE_CUENTAS = (
      (AHORROS,'Ahorros'),
      (CORRIENTE,'Corriente'),
      (OTRA,'Otra'),
   )
   cliente = models.ForeignKey(Cliente)
   tipo = models.SmallIntegerField(choices=TIPOS_DE_CUENTAS,default=AHORROS)
   numero_cuenta = models.CharField(max_length=30)

   def get_saldo(self):
      # entradas 
      valor = Transaccion.objects.filter(cuenta=self,tipo=Transaccion.CONSIGNACION).aggregate(Sum('valor'))['valor__sum'] or 0
      valor += Transaccion.objects.filter(cuenta_destino=self,tipo=Transaccion.TRANSFERENCIA).aggregate(Sum('valor'))['valor__sum'] or 0
      # salidas
      valor -= Transaccion.objects.filter(cuenta=self,tipo=Transaccion.RETIRO).aggregate(Sum('valor'))['valor__sum'] or 0
      valor -= Transaccion.objects.filter(cuenta=self,tipo=Transaccion.TRANSFERENCIA).aggregate(Sum('valor'))['valor__sum'] or 0
      return round(valor,2)

   def get_tarjeta_debito(self):
      tarjeta = self.tarjetadebito_set.filter(estado_registro=True).order_by('-fecha_registro')
      return tarjeta[0] if tarjeta else None

   def __unicode__(self):
      return unicode(self.cliente)+" - "+unicode(self.numero_cuenta)

class TarjetaDebito(ModeloBase):
   numero = models.CharField(max_length=30,unique=True)
   cuenta = models.ForeignKey(Cuenta)

   def save(self):
      if not self.id:
         tarjetas = self.cuenta.tarjetadebito_set.all()
         for t in  tarjetas:
            t.estado_registro= False
            t.save()
      super(TarjetaDebito,self).save()

   def __unicode__(self):
      return unicode(self.cuenta)+" - "+unicode(self.numero) 

class Transaccion(ModeloBase):
   TRANSFERENCIA = 1
   CONSIGNACION = 2
   RETIRO = 3
   TIPOS_TRANSACCION = (
      (TRANSFERENCIA,'Transeferencia'),
      (CONSIGNACION,'Consignación'),
      (RETIRO,'Retiro'),
   )
   banco = models.ForeignKey(Banco)
   tipo = models.SmallIntegerField(choices=TIPOS_TRANSACCION)
   cuenta = models.ForeignKey(Cuenta,related_name='cuenta')
   cuenta_destino = models.ForeignKey(Cuenta,related_name='cuenta_destino',null=True,blank=True)
   valor = models.FloatField()

   def get_clase(self,cliente=None):
      if self.tipo == self.RETIRO:
         return 'valor_negativo'
      if self.tipo == self.CONSIGNACION:
         return 'valor_positivo'
      if self.tipo == self.TRANSFERENCIA:
         if cliente:
            if self.cuenta_destino.cliente == cliente:
               return 'valor_positivo'
            return 'valor_negativo'
         return "valor_neutro"

   def __unicode__(self):
      return unicode(self.get_tipo_display())+" - "+unicode(self.cuenta)
