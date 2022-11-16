from django.contrib import admin
from .models import Usuarios,Transferencia,Instituicao


# Register your models here.

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    ...

@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    ...
    
@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    ...
    



