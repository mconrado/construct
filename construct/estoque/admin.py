import imp
from django.contrib import admin
from .models import Categoria, Imagem, Produto

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Imagem)