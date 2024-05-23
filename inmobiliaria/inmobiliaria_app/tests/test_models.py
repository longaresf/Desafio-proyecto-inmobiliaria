from django.test import TestCase
from django.db import models
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image

# Create your models here.

# class UsuarioModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Usuario.objects.create(rut='111111111', nombres='Juan Pedro', apellidos='Aguilar Silva', direccion='Pandora 3212, Maipu, Santiago', telefono='999999999', email='juan@mail.cl', tipo_user='Arrendatario', activo='True', creado_por='Admin')

#         Inmueble.objects.create(nombre='Departamento Francisco De Villagra', descripcion='No amoblado, 1 dormitorio, 1 baño, No Admite mascotas, 1 estacionamiento, Año de construcción: 2015', m2_construidos=28, m2_totales=33, cant_estacionamientos='1', cant_habitaciones='1', cant_banios='1', direccion='Francisco De Villagra', comuna='Ñuñoa', tipo_inmueble='Departamento', precio_mes_arriendo=530000, activo=True, creado_por='Admin')

#     def test_rut_label(self):
#         user=Usuario.objects.get(rut='111111111')
#         field_label = user._meta.get_field('rut').verbose_name
#         self.assertEqual(field_label,'rut')

#     def test_rut_max_length(self):
#         user=Usuario.objects.get(rut='111111111')
#         max_length = user._meta.get_field('rut').max_length
#         self.assertEqual(max_length,9)

#     def test_object_name_is_first_name_comma_last_name(self):
#         user=Usuario.objects.get(rut='111111111')
#         expected_object_name = '%s, %s' % (user.apellidos, user.nombres)
#         self.assertEqual(expected_object_name,str(user))

#     def test_object_arrendatario(self):
#         user_inm=Usuario_Inmueble.objects.get(id='1')
#         expected_object_name = '%s, %s' % ("Arrendatario: " + user_inm.arrendatario.nombres + "" + user_inm.arrendatario.apellidos + " Propiedad: " +  user_inm.inmueble.nombre + " en la comuna de " + user_inm.inmueble.comuna)
#         self.assertEqual(expected_object_name,str(user_inm))
        