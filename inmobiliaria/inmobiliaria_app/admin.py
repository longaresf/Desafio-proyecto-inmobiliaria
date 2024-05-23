from django.contrib import admin
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Inmueble)
admin.site.register(Usuario_Inmueble)
admin.site.register(Comuna)
admin.site.register(Provincia)
admin.site.register(Region)
admin.site.register(Image)