# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from banco.models import *
# Register your models here.

admin.site.register(Banco)
admin.site.register(Cliente)
admin.site.register(Cuenta)
admin.site.register(TarjetaDebito)
admin.site.register(Transaccion)