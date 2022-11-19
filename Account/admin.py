from django.contrib import admin
from .models import Conta, Transferencia, Instituicao


# Register your models here.

@admin.register(Conta)
class UsuariosAdmin(admin.ModelAdmin):
    ...

@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    ...

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    ...
