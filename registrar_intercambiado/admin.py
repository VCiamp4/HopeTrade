from django.contrib import admin
from .models import Intercambiador, Ayudante, Filial, Categoria, Publicacion, Intercambio

# Register your models here.

admin.site.register(Intercambiador)
admin.site.register(Ayudante)
admin.site.register(Publicacion)
admin.site.register(Filial)
admin.site.register(Categoria)
admin.site.register(Intercambio)
