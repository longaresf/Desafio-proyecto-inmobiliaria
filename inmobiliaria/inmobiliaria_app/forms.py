from django import forms
from django.forms import ModelForm, ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column


INMUEBLES = (('Casa', 'Casa'),
                 ('Departamento', 'Departamento'),
                 ('Parcela', 'Parcela'))

USUARIO = (('Arrendador', 'Arrendador'),
                 ('Arrendatario', 'Arrendatario'))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63,
         label = 'Usuario',
     )
    password = forms.CharField(max_length=89,
        widget=forms.PasswordInput,
         label = 'Password',
     )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit = True):
        user = super().save()
        self.save_m2m()
        return user
    
class SearchForm(forms.Form):
    inmueble_tipo = forms.ChoiceField(
        choices=INMUEBLES,
         label = '',
     )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
         label = '',
     )
    ciudad = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
         label = '',
     )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
         label = '',
     )
    
    
class UserForm(forms.ModelForm):
    
    tipo_user = forms.ChoiceField(
        choices=USUARIO,
         label = 'Tipo',
     )
    
    class Meta:
        model = Usuario
        fields = ('rut', 'nombres', 'apellidos', 'direccion', 'telefono', 'email', 'tipo_user', 'activo', 'usuario', 'creado_por')


class InmForm(forms.ModelForm):
    
    construido = forms.CharField(
         label = 'Área Construida',
     )
    totales = forms.CharField(
         label = 'Área Total',
     )
    banios = forms.CharField(
         label = 'Baños',
     )
    direccion = forms.CharField(
         label = 'Dirección',
     )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
         label = 'Comuna',
     )
    inmueble_tipo = forms.ChoiceField(
        choices=INMUEBLES,
         label = 'Tipo',
     )
    arriendo_mes = forms.CharField(
         label = 'Arriendo Mensual',
     )

    class Meta:
        model = Inmueble
        fields = ('nombre', 'descripcion', 'construido', 'totales', 'estacionamiento', 'habitaciones', 'banios', 'direccion', 'comuna', 'inmueble_tipo', 'arriendo_mes', 'activo', 'usuario', 'creado_por')


class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = ('image', 'inmueble')

    
    