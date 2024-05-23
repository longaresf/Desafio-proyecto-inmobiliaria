from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout, authenticate, login
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image
from django.contrib import messages
from inmobiliaria_app.forms import LoginForm, CustomUserCreationForm, UserForm, InmForm, ImageForm, SearchForm
from django.contrib.auth.models import Group, User
from inmobiliaria_app.services import crear_usuario, update_usuario, crear_inmueble
from django.core.exceptions import ValidationError

# Create your views here.

def home(request):
    inm = Inmueble.objects.filter(activo=True)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            inmueble_tipo=request.POST.get('inmueble_tipo')
            comuna=request.POST.get('comuna')
            ciudad=request.POST.get('ciudad')
            region=request.POST.get('region')
            inm = Inmueble.objects.filter(comuna=comuna)
            print(f'{inm}')
            #return render(request, 'home.html', {'inm':inm, 'form':form})
    else:
        form = SearchForm()
    return render(request, 'home.html', {'inm':inm, 'form':form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.warning(request, "Usuario o contraseña errada")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form':form })

def salir(request):
    logout(request)
    return redirect('/')

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form_2 = CustomUserCreationForm(request.POST)
        
        if form_2.is_valid() and form.is_valid():
            crear_usuario(form, form_2)
            user = authenticate(username = form_2.cleaned_data['username'], password = form_2.cleaned_data['password1'])
            login(request,user)

            messages.success(request, "Registro exitoso. Gracias por registrarte a Inmobiliaria Francisco!")
            return redirect('/')
        else:
            messages.warning(request, "Falló registro, favor intentar nuevamente")
    else:
        form_2 = CustomUserCreationForm()
        form = UserForm()
    return render(request, "register_user.html", { 'form_2':form_2, 'form':form  })

def update_user(request):
    user = User.objects.get(pk=request.user.id)
    try:
        usuario = Usuario.objects.get(usuario=request.user.id)
    except User.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")
    except Usuario.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=usuario)

        if form.is_valid():
            update_usuario(form)
            messages.success(request, "Registro mofificado exitosamente.")
        else:
            messages.warning(request, "Hubo un problema, favor intentar nuevamente")
    else:
        form = UserForm()
    return render(request, "update_user.html", { 'form':form, 'usuario':usuario })

def perfil_user(request):
    user = User.objects.get(pk=request.user.id)
    try:
        usuario = Usuario.objects.get(usuario=request.user.id)
        if usuario.tipo_user == 'Arrendatario':
            inm = Inmueble.objects.filter(usuario=request.user.id)
    except Usuario.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")
    except User.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")     
    except Inmueble.DoesNotExist:
            messages.warning(request, "Usuario no posee publicaciones")
    form = UserForm()
    return render(request, "perfil_user.html", { 'form':form, 'user':user, 'usuario':usuario })
    
def delete_user(request):
    user = User.objects.get(pk=request.user.id)
    user.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('/')

def create_inm(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = InmForm(request.POST)
        if form.is_valid():
            crear_inmueble(form, user)
 
            messages.success(request, "Registro de inmueble creado correctamente.")
            return redirect('image_add.html')
        else:
            messages.warning(request, "Falló registro, favor intentar nuevamente")
    else:
        form = InmForm()
    return render(request, "create_inm.html", { 'form':form, 'user':user })

def image_inmueble(request):
    inm_id = Inmueble.objects.latest('id').id
    inm = Inmueble.objects.get(pk=inm_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            img_object=form.instance
            img= Image.objects.filter(inmueble_id=inm_id)
            messages.success(request, "Imajen agregada correctamente.")
            return render(request, 'image_add.html', {'form': form, 'img_obj': img_object, 'img':img })
        else:
            messages.warning(request, "Falló registro, favor intentar nuevamente")
    else:
        form = ImageForm()
    return render(request, "image_add.html", { 'form':form, 'inm':inm })

def publication_inm(request):
    user_id = User.objects.get(pk=request.user.id)
    inm = Inmueble.objects.filter(usuario=user_id.id)
    print(f'inm: {inm}')
    return render(request, "publication_inm.html", { 'inm':inm })

def perfil_inm(request, id):
    inm = Inmueble.objects.get(pk=id)
    form = UserForm()
    return render(request, "perfil_inm.html", { 'form':form, 'inm':inm })

def update_inm(request, id):
    inm = Inmueble.objects.filter(pk=id)
    if request.method == 'POST':
        form = InmForm(request.POST, instance=inm)
        if form.is_valid():
            form.save()
            messages.success(request, "Actualizado correctamente.")
        else:
            messages.warning(request, "Algo falló, favor intentar nuevamente")
    else:
        form = InmForm()
    return render(request, "update_inm.html", { 'form':form, 'inm':inm })








def delete_inm(request, id):
    inm = InmForm.objects.get(pk=id)
    inm.delete()
    messages.success(request, "Inmueble eliminado correctamente.")
    return redirect('/')

def delete_img(request,id):
    delete_img = Image.objects.get(pk=id)
    delete_img.delete()
    messages.success(request, "Imagen eliminada correctamente.")
    return delete_img







def bad_request(request, exception=None):
    # return render(request, '400.html')
    return redirect('/')

def permission_denied(request, exception=None):
    # return render(request, '403.html')
    return redirect('/')

def page_not_found(request, exception=None):
    # return render(request, '404.html')
    return redirect('/')

def server_error(request, exception=None):
    # return render(request, '500.html')
    return redirect('/')







# user = User.objects.get(pk=form['usuario'].value())
#return render(request, "register_usuario.html", { "mensaje_1":"Gracias por registrarte a Inmobiliaria Francisco!", "mensaje_2": "Favor completa tu registro y utiliza nuestra plataforma", 'user':user })

# def register_arrendador(request):
#     data = {"form": CustomUserCreationForm()}
#     if request.method == 'POST':
#         user_creation_form = CustomUserCreationForm(data=request.POST)
#         if user_creation_form.is_valid():
#             user = user_creation_form.save()
#             group = Group.objects.get(name='Arrendador')
#             user.groups.add(group)
#             user = authenticate(username = user_creation_form.cleaned_data['username'], password = user_creation_form.cleaned_data['password1'])
#             login(request,user)
#             return render(request, "mensaje/mensaje.html", {"mensaje":"Gracias por registrarte Arrendador"})
#     return render(request, "register_user.html", data)

# def update_data_user(request):
#     user = User.objects.get(pk={{user.id}})
#     user_groups = Group.objects.get(user={{user.id}})
#     data = {"form": UserForm()}
#     if request.method == 'POST':
#         user_creation_form = UserForm(data=request.POST)
#         if user_creation_form.is_valid():
# 
#             # user = user_creation_form.save()
#             # user = authenticate(username = user_creation_form.cleaned_data['username'], password = user_creation_form.cleaned_data['password1'])
#             # login(request,user)
#             return render(request, "mensaje/mensaje.html", {"mensaje":"Gracias por actualizar Arrendador"})
#     return render(request=request, template_name="update_user.html", context={ 'data':data, 'user':user, 'user_groups':user_groups})

# def update_user(request, rut):
#     user = Usuario.objects.get(rut=rut)
#     data = {"form": UserForm(instance=user)}
#     if request.method == 'POST':
#         user_upd_form = UserForm(data=request.POST, instance=user)
#         if user_upd_form.is_valid():
#             user_upd_form.save()
#             return render(request, "mensaje/mensaje.html", {"mensaje":"Gracias por actualizar {{user.nombres}}"})
#     return render(request=request, template_name="update_user.html", context={ 'data':data, 'user':user })

# def register_usuario(request):
#     data = {"form": CustomUserCreationForm()}
#     if request.method == 'POST':
#         user_creation_form = CustomUserCreationForm(data=request.POST)
#         if user_creation_form.is_valid():
#             user = user_creation_form.save()
#             group = Group.objects.get(name='Arrendatario')
#             user.groups.add(group)
#             user = authenticate(username = user_creation_form.cleaned_data['username'], password = user_creation_form.cleaned_data['password1'])
#             login(request,user)
#             return render(request, "mensaje/mensaje.html", {"mensaje":"Gracias por registrarte Arrendatario"})
#     return render(request, "register.html", data)



