from django.db import models
from django.contrib.auth.models import Group, User
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image
from django.contrib.auth.hashers import make_password


def crear_usuario(form, form_2):
    user = User.objects.create(username=form_2['username'].value(), first_name=form['nombres'].value(), last_name=form['apellidos'].value(), email=form['email'].value(), password=make_password(form_2['password1'].value()))

    user_id = User.objects.get(id=user.id)
    group = Group.objects.get(name=form['tipo_user'].value())
    user.groups.add(group)
        
    usuario = Usuario.objects.create(rut=form['rut'].value(), nombres=form['nombres'].value(), apellidos=form['apellidos'].value(), direccion=form['direccion'].value(), telefono=form['telefono'].value(), email=form['email'].value(), tipo_user=form['tipo_user'].value(), activo=form['activo'].value(), usuario=user_id, creado_por=form['creado_por'].value())

    return user_id

def update_usuario(form):
    id = form['usuario'].value()
    user = User.objects.filter(pk=id).update(first_name=form['nombres'].value(), last_name=form['apellidos'].value(), email=form['email'].value())

    group = Group.objects.get(name=form['tipo_user'].value())
    group.user_set.add(user)
    
    usuario = Usuario.objects.filter(usuario=id).update(nombres=form['nombres'].value(), apellidos=form['apellidos'].value(), direccion=form['direccion'].value(), telefono=form['telefono'].value(), email=form['email'].value(), tipo_user=form['tipo_user'].value())
    
    return usuario

def crear_inmueble(form, user):
    comuna = Comuna.objects.get(id=form['comuna'].value())

    inm = Inmueble.objects.create(nombre=form['nombre'].value(), descripcion=form['descripcion'].value(), construido=form['construido'].value(), totales=form['totales'].value(), estacionamiento=form['estacionamiento'].value(), habitaciones=form['habitaciones'].value(), banios=form['banios'].value(), direccion=form['direccion'].value(), comuna=comuna, inmueble_tipo=form['inmueble_tipo'].value(), arriendo_mes=form['arriendo_mes'].value(), activo=form['activo'].value(), creado_por=form['creado_por'].value())
    
    inm_id = Inmueble.objects.latest('id').id
    inm = Inmueble.objects.get(pk=inm_id)
    user_id = User.objects.filter(pk=user.id)

    inm.usuario.set(user_id)

    return inm





def lista_propiedades_comuna(comuna):
    inmuebles = Inmueble.objects.filter(comuna=comuna)
    return inmuebles

def listar_propiedades():
    inmuebles = list(Inmueble.objects.all())
    return inmuebles

def update_inmueble(id, nombre, descripcion, construidos, totales, estacionamiento, habitaciones, banios, direccion, comuna, inmueble_tipo, arriendo_mes, activo, creado_por):
    update_inmueble = Inmueble.objects.filter(pk=id).update(nombre=nombre, descripcion=descripcion, construidos=construidos, totales=totales, estacionamiento=estacionamiento, habitaciones=habitaciones, banios=banios, direccion=direccion, comuna=comuna, inmueble_tipo=inmueble_tipo, arriendo_mes=arriendo_mes, activo=activo, creado_por=creado_por)
    return update_inmueble






def eliminar_propiedades(inmueble):
    eliminar_inmueble = Inmueble.objects.get(pk=inmueble)
    eliminar_inmueble.delete()
    return eliminar_inmueble

def solicitud_arriendo(rut, inmueble):
    arrendatario = Usuario.objects.get(pk=rut)
    inmueble = Inmueble.objects.get(pk=inmueble)
    Solicitud_arriendo = Usuario_Inmueble.objects.create(arrendatario=arrendatario, inmueble=inmueble, creado_por=arrendatario)
    return Solicitud_arriendo

def listar_estado_propiedades(estado):
        inmueble = list(Usuario_Inmueble.objects.all().filter(estado=estado))
        print(f'inmueble: {inmueble}')

def eliminar_propiedad_por_aprobacion_arriendo(id):
    eliminar_solicitud_arriendo = Usuario_Inmueble.objects.get(id=id)
    eliminar_solicitud_arriendo.delete()
    return eliminar_solicitud_arriendo

def aceptar_arrendatario(rut, id, estado):
    inmueble = Inmueble.objects.get(id=id)
    arrendatario = Usuario.objects.get(pk=rut)
    try:
        arriendo = Usuario_Inmueble.objects.filter(inmueble=id, arrendatario=rut).get(estado=estado)
        if arriendo.estado == 'Pendiente':
            arriendo = Usuario_Inmueble.objects.filter(inmueble=id, arrendatario=rut).update(estado='Aprobado')
            print('Se ha Aceptado el Arrendatario')
            return arriendo
        elif arriendo.estado == 'Rechazado':
            print('Arriendo fue Rechazado')
        else:
            print('El Arrendatario ya fue Aceptado anteriormente')
    except:
        print(f'Arrendatario no presenta inmueble en estado: {estado}')    

def print_inmueble_comuna():
    inmueble_comuna = Inmueble.objects.values_list('comuna', 'nombre', 'descripcion')
    
    comunas = sorted(set([i[0] for i in inmueble_comuna]))
    for comuna in comunas:
        print(f"Comuna: {comuna}")
        for dato in [j for j in inmueble_comuna if j[0]==comuna]:
            print(f"\tNombre: {dato[1]} \n\tDescripción: {dato[2]}")
            
    f=open("inmueble_comuna.txt","a", encoding="utf-8")
    for i in inmueble_comuna:
        f.write(str(i[0]))
        f.write(',')
        f.write(str(i[1]))
        f.write(',')
        f.write(str(i[2]))
        f.write("\n")
    f.close()

def print_inmueble_region():
    inm_com = Inmueble.objects.values_list('comuna')
    for c in inm_com:
        inmueble_com = Inmueble.objects.get(comuna=c[0])
        inmueble = Inmueble.objects.get(id=inmueble_com.id)
        comuna_nom = Comuna.objects.get(nombre=c[0])
        comuna = Comuna.objects.get(id=comuna_nom.id)
        
        #print(f'Inmueble: {inmueble.nombre}, {comuna.nombre}, {comuna_nom.comuna_provincia.nombre}, {comuna_nom.comuna_provincia.provincia_region.nombre}')
        # comunas print(f'{(str(c[0]))}')
        #print(f'{(str(inmueble.nombre))}')
     
        f=open("inmueble_regiones.txt","a", encoding="utf-8")
        f.write(f'Inmueble: {inmueble.nombre}, {comuna.nombre}, {comuna_nom.comuna_provincia.nombre}, {comuna_nom.comuna_provincia.provincia_region.nombre}')
        f.write("\n")
    f.close()
    
    
def delete_img(id):
    delete_img = Image.objects.get(pk=id)
    delete_img.delete()
    return delete_img

def image_inm(form):
    inm_id = Inmueble.objects.latest('id').id
    inm= Inmueble.objects.get(pk=inm_id)
    image_add = Image.objects.create(image=form['image'].value(), inmueble=inm)
    
    return image_add
