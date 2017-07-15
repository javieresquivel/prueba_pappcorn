# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
# Create your models here.

class Usuario(AbstractUser):
   direccion = models.CharField(null=True,blank=True,max_length=50)
   telefono = models.CharField(max_length=50,null=True,blank=True)
   # Foto usuario
   foto = ResizedImageField(size=[1800, 1500], upload_to='fotos_usuario', null=True,blank=True)
   foto_sm = ResizedImageField(size=[320, 320], upload_to='fotos_usuario/sm', null=True,blank=True)
   foto_xs = ResizedImageField(size=[100, 100], upload_to='fotos_usuario/xm', null=True,blank=True)

   class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

   def set_foto(self):
      self.foto_sm = self.foto
      self.foto_xs = self.foto
      super(Usuario, self).save()