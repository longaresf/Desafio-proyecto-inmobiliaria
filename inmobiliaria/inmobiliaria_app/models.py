from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class Region(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return '%s' % (self.nombre)

class Provincia(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=23, null=False, blank=False)
    region = models.ForeignKey(Region, related_name = 'reg', on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s' % (self.nombre)
    
class Comuna(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    provincia = models.ForeignKey(Provincia, related_name = 'prov', on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s' % (self.nombre)
    
class Usuario(models.Model):
    rut = models.CharField(max_length=9, primary_key=True, null=False)
    nombres = models.CharField(max_length=30, null=False, blank=False)
    apellidos = models.CharField(max_length=30, null=False, blank=False)
    direccion = models.CharField(max_length=80, null=False, blank=False)
    telefono = models.CharField(max_length=16, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)

    USUARIO = (('Arrendador', 'Arrendador'),
                 ('Arrendatario', 'Arrendatario'))
    tipo_user = models.CharField(choices=USUARIO, default='Arrendador', max_length=12)
    activo = models.BooleanField(default=False)
    usuario = models.OneToOneField(User, related_name = 'usuario', on_delete=models.CASCADE, unique=True)
    crea_regist = models.DateField(auto_now_add=True)
    mod_regist = models.DateField(auto_now=True)
    creado_por = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return '%s, %s' % (self.apellidos, self.nombres)

class Inmueble(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=80, null=False, blank=False)
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    construido = models.IntegerField(null=False, blank=False)
    totales = models.IntegerField(null=False, blank=False)
    estacionamiento = models.CharField(max_length=2, null=False, blank=False)
    habitaciones = models.CharField(max_length=2, null=False, blank=False)
    banios = models.CharField(max_length=2, null=False, blank=False)
    direccion = models.CharField(max_length=80, null=False, blank=False)
    comuna = models.ForeignKey(Comuna, related_name = 'com', on_delete=models.CASCADE)

    INMUEBLES = (('Casa', 'Casa'),
                 ('Departamento', 'Departamento'),
                 ('Parcela', 'Parcela'))
    inmueble_tipo = models.CharField(choices=INMUEBLES, default='Departamento', max_length=12)
    arriendo_mes = models.IntegerField(null=False, blank=False)
    activo = models.BooleanField(default=False)
    usuario = models.ManyToManyField(User, related_name='imn_user', through='Usuario_Inmueble')
    crea_regist = models.DateField(auto_now_add=True)
    mod_regist = models.DateField(auto_now=True)
    creado_por = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.nombre + ". Comuna: " + self.comuna.nombre

class Image(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    image = models.ImageField(upload_to='inmobiliaria/')
    inmueble = models.ForeignKey(Inmueble, related_name = 'inm', on_delete=models.CASCADE)

class Usuario_Inmueble(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    arrendatario = models.ForeignKey(User, related_name = 'arrendata', on_delete=models.CASCADE)
    arrendador = models.ForeignKey(Usuario, related_name = 'arrendado', on_delete=models.CASCADE, null=True, blank=True)
    inmueble = models.ForeignKey(Inmueble, related_name = 'inmueble', on_delete=models.CASCADE)

    ESTADO =    (('0', 'Aprobado'),
                 ('1', 'Rechazado'),
                 ('2', 'Pendiente'))
    estado = models.CharField(choices=ESTADO, default='Pendiente', max_length=12)
    crea_regist = models.DateField(auto_now_add=True)
    mod_regist = models.DateField(auto_now=True)
    creado_por = models.CharField(max_length=50, null=False)

    def __str__(self):
        return "Arrendatario: " + self.arrendatario.nombres + "" + self.arrendatario.apellidos + " Propiedad: " +  self.inmueble.nombre + " en la comuna de " + self.inmueble.comuna
