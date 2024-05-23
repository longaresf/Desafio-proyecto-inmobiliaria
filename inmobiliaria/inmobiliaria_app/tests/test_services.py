from django.test import TestCase
from django.db import models
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image
from inmobiliaria_app.services import crear_usuario, crear_inmueble, lista_propiedades_comuna, solicitud_arriendo, listar_propiedades, update_inmueble, eliminar_propiedades, aceptar_arrendatario, listar_estado_propiedades, eliminar_propiedad_por_aprobacion_arriendo, print_inmueble_comuna, add_image_inmueble, print_inmueble_region

class ServicesTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # nuevo_arrendador = Usuario.objects.create(rut='222222222', nombres='Elizabeth', apellidos='Barre', direccion='Juncal 455, Cerrillo, Santiago', telefono='988888888', email='eli@mail.cl', tipo_user='Arrendador', activo='True', creado_por='Admin')

        # nuevo_arrendatario = Usuario.objects.create(rut='111111111', nombres='Juan Pedro', apellidos='Aguilar Silva', direccion='Pandora 3212, Maipu, Santiago', telefono='999999999', email='juan@mail.cl', tipo_user='Arrendatario', activo='True', creado_por='Admin')

        # nuevo_inmueble = Inmueble.objects.create(nombre='Departamento Francisco De Villagra', descripcion='No amoblado, 1 dormitorio, 1 baño, No Admite mascotas, 1 estacionamiento, Año de construcción: 2015', m2_construidos=28, m2_totales=33, cant_estacionamientos='1', cant_habitaciones='1', cant_banios='1', direccion='Francisco De Villagra', comuna='Ñuñoa', tipo_inmueble='Departamento', precio_mes_arriendo=530000, activo=True, creado_por='Admin')
        pass
    

    
    def test_crear_arrendador(self):
        nuevo_arrendador = Usuario.objects.create(rut='222222222', nombres='Elizabeth', apellidos='Barre', direccion='Juncal 455, Cerrillo, Santiago', telefono='988888888', email='eli@mail.cl', tipo_user='Arrendador', activo='True', creado_por='Admin')
        self.assertEqual(nuevo_arrendador.nombres, 'Elizabeth')

    def test_crear_arrendatario(self):
        nuevo_arrendatario = Usuario.objects.create(rut='111111111', nombres='Juan Pedro', apellidos='Aguilar Silva', direccion='Pandora 3212, Maipu, Santiago', telefono='999999999', email='juan@mail.cl', tipo_user='Arrendatario', activo='True', creado_por='Admin')
        self.assertEqual(nuevo_arrendatario.nombres, 'Juan Pedro')

    def test_crear_inmueble(self):
        nuevo_inmueble = Inmueble.objects.create(nombre='Departamento Francisco De Villagra', descripcion='No amoblado, 1 dormitorio, 1 baño, No Admite mascotas, 1 estacionamiento, Año de construcción: 2015', m2_construidos=28, m2_totales=33, cant_estacionamientos='1', cant_habitaciones='1', cant_banios='1', direccion='Francisco De Villagra', comuna='Ñuñoa', tipo_inmueble='Departamento', precio_mes_arriendo=530000, activo=True, creado_por='Admin')
        self.assertEqual(nuevo_inmueble.nombre, 'Departamento Francisco De Villagra')
    
    def test_update_inmueble(self):
        update_inmueble = Inmueble.objects.update(nombre='Nombre_update', descripcion='descripcion_update', m2_construidos=22, m2_totales=44, cant_estacionamientos='1', cant_habitaciones='1', cant_banios='1', direccion='Francisco De Villagra', comuna='Ñuñoa', tipo_inmueble='Departamento', precio_mes_arriendo=530000, activo=True, creado_por='Admin')
        self.assertEqual(update_inmueble, 1)
    
    def test_lista_propiedades_comuna(self):
        inmuebles_comuna = Inmueble.objects.filter(comuna='Ñuñoa')
        for i in inmuebles_comuna:
            self.assertEqual(i.nombre, 'Departamento Francisco De Villagra')

    def test_listar_propiedades(self):
        inmuebles = Inmueble.objects.all()
        for i in inmuebles:
            self.assertEqual(i.nombre, 'Departamento Francisco De Villagra')

    def solicitud_arriendo(self):
        arrendatario = Usuario.objects.get(rut='111111111')
        inmueble = Inmueble.objects.get(id=1)
        Solicitud_arriendo = Usuario_Inmueble.objects.create(arrendatario='111111111', inmueble=1, creado_por='Juan Pedro')
        self.assertEqual(Solicitud_arriendo.estado, 'Pendiente')

    def setUp(self):
        nuevo_arrendador = Usuario.objects.create(rut='222222222', nombres='Elizabeth', apellidos='Barre', direccion='Juncal 455, Cerrillo, Santiago', telefono='988888888', email='eli@mail.cl', tipo_user='Arrendador', activo='True', creado_por='Admin')

        nuevo_arrendatario = Usuario.objects.create(rut='111111111', nombres='Juan Pedro', apellidos='Aguilar Silva', direccion='Pandora 3212, Maipu, Santiago', telefono='999999999', email='juan@mail.cl', tipo_user='Arrendatario', activo='True', creado_por='Admin')

        nuevo_inmueble = Inmueble.objects.create(nombre='Departamento Francisco De Villagra', descripcion='No amoblado, 1 dormitorio, 1 baño, No Admite mascotas, 1 estacionamiento, Año de construcción: 2015', m2_construidos=28, m2_totales=33, cant_estacionamientos='1', cant_habitaciones='1', cant_banios='1', direccion='Francisco De Villagra', comuna='Ñuñoa', tipo_inmueble='Departamento', precio_mes_arriendo=530000, activo=True, creado_por='Admin')

    def test_aceptar_arrendatario(self):
        inmueble = Inmueble.objects.get(id=1)
        arrendatario = Usuario.objects.get(rut='111111111')
        try:
            arriendo = Usuario_Inmueble.objects.filter(inmueble=1, arrendatario='111111111').get(estado='Pendiente')
            if arriendo.estado == 'Pendiente':
                arriendo = Usuario_Inmueble.objects.filter(inmueble=1, arrendatario='111111111').update(estado='Aprobado')
                print('Se ha Aceptado el Arrendatario')
                self.assertEqual(arriendo.estado, 'Aprobado')
            elif arriendo.estado == 'Rechazado':
                print('Arriendo fue Rechazado')
            else:
                print('El Arrendatario ya fue Aceptado anteriormente')
        except:
            print(f'Arrendatario no presenta inmueble en estado: Aceptado')    

    # def setUp(self):
    #     nuevo_arrendador = Usuario.objects.create(rut='222222222', nombres='Elizabeth', apellidos='Barre', direccion='Juncal 455, Cerrillo, Santiago', telefono='988888888', email='eli@mail.cl', tipo_user='Arrendador', activo='True', creado_por='Admin')

    #     nuevo_arrendatario = Usuario.objects.create(rut='111111111', nombres='Juan Pedro', apellidos='Aguilar Silva', direccion='Pandora 3212, Maipu, Santiago', telefono='999999999', email='juan@mail.cl', tipo_user='Arrendatario', activo='True', creado_por='Admin')

    #     nuevo_inmueble = Inmueble.objects.create(nombre='Departamento Francisco De Villagra', descripcion='No amoblado, 1 dormitorio, 1 baño, No Admite mascotas, 1 estacionamiento, Año de construcción: 2015', m2_construidos=28, m2_totales=33, cant_estacionamientos='1', cant_habitaciones='1', cant_banios='1', direccion='Francisco De Villagra', comuna='Ñuñoa', tipo_inmueble='Departamento', precio_mes_arriendo=530000, activo=True, creado_por='Admin')

    # def test_eliminar_propiedades(self):
    #     eliminar_inmueble = Inmueble.objects.get(id=2)
    #     self.assertEqual(eliminar_inmueble.nombre, 'Departamento Francisco De Villagra')
    