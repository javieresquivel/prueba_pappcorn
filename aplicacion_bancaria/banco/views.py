# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from banco.models import *
from forms import *
# Create your views here.
class InicioView(View):

   def agregar(self,request):
      formulario = BancoForm(request.POST)
      if formulario.is_valid():
         banco = formulario.save(commit=False)
         banco.usuario_registro = request.user
         banco.save()
         bancos = Banco.objects.filter(estado_registro=True)
         return render(request, 'render/tabla_bancos.html', locals())
      if formulario.errors:
         return JsonResponse({"mensaje":unicode(formulario.errors)}) 
      return render(request, 'inicio.html', locals())

   def eliminar_banco(self,request):
      banco = get_object_or_404(Banco,pk=request.POST["eliminar_banco"])
      banco.delete()
      bancos = Banco.objects.filter(estado_registro=True)
      return render(request, 'render/tabla_bancos.html', locals())

   def validar_codigo(self,request):
      codigo = request.POST["validar_codigo"].upper()
      if Banco.objects.filter(codigo=codigo):
         return HttpResponse("El codigo "+unicode(codigo)+" ya se encuentra registrado",status=500)
      return HttpResponse("El codigo "+unicode(codigo)+" esta disponible")

   def get(self,request):
      formulario = BancoForm()
      bancos = Banco.objects.filter(estado_registro=True)
      return render(request, 'inicio.html', locals())

   def post(self,request):
      if 'agregar_banco' in request.POST and 'banco.add_banco' in request.user.get_all_permissions():
         return self.agregar(request)
      if 'validar_codigo' in request.POST:
         return self.validar_codigo(request)
      if 'eliminar_banco' in request.POST and 'banco.delete_banco' in request.user.get_all_permissions():
         return self.eliminar_banco(request)
      return HttpResponse("No posee los permisos para esta funcion",status=403)

class ClientesView(View):

   def agregar(self,request,banco):
      formulario = ClienteForm(request.POST or None, banco=banco)
      if formulario.is_valid():
         cliente = formulario.save(commit=False)
         cliente.banco = banco
         cliente.usuario_registro = request.user
         cliente.save()
         # Cuentas
         for item in formulario.cleaned_data.get("cuentas"):
            # Cuenta
            item["cuenta"].cliente = cliente
            item["cuenta"].usuario_registro = request.user
            item["cuenta"].save()
            # Tarjeta
            item["tarjeta"].cuenta= item["cuenta"]
            item["tarjeta"].usuario_registro = request.user
            item["tarjeta"].save()
         return HttpResponseRedirect("/bancos/clientes?banco="+str(banco.id)+"&ver_cliente="+str(cliente.id))

      return render(request, 'clientes/agregar_nuevo_cliente.html', locals())

   def ver(self,request,banco):
      cliente = get_object_or_404(Cliente,pk=request.GET['ver_cliente'])
      return render(request, 'clientes/ver_cliente.html', locals())

   def get(self,request):
      banco = get_object_or_404(Banco,pk=request.GET["banco"])
      if 'agregar' in request.GET and 'banco.add_cliente' in request.user.get_all_permissions():
         return self.agregar(request,banco)
      if 'ver_cliente' in request.GET:
         return self.ver(request,banco)
      clientes = Cliente.objects.filter(estado_registro=True,banco=banco)
      return render(request, 'clientes/listado_clientes.html', locals())
      
   def post(self,request):
      banco = get_object_or_404(Banco,pk=request.GET["banco"])
      if 'agregar' in request.GET and 'banco.add_cliente' in request.user.get_all_permissions():
         return self.agregar(request,banco)
      return HttpResponse("No posee los permisos para esta funcion",status=403)

class TransaccionesView(View):

   def agregar(self,request):
      formulario = TransaccionForm(request.POST or None)
      if formulario.is_valid():
         pass
      return render(request, 'transacciones/agregar_transaccion.html', locals())

   def get(self,request):
      if 'agregar' in request.GET:
         return self.agregar(request)
      transacciones = Transaccion.objects.filter(estado_registro=True).order_by('-fecha_registro')
      return render(request, 'transacciones/listado_transacciones.html', locals())
      
   def post(self,request):
      if 'agregar' in request.GET:
         return self.agregar(request)
      return HttpResponse("No posee los permisos para esta funcion",status=403)