"""
URL configuration for inmobiliaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from inmobiliaria_app.views import login_page, salir, home, register_user, update_user, perfil_user, create_inm, update_inm, perfil_inm, image_inmueble, delete_user, delete_inm, bad_request, permission_denied, page_not_found, server_error, delete_img, publication_inm
from django.conf.urls import handler400, handler403, handler404, handler500

handler404 = 'inmobiliaria_app.views.page_not_found'
handler500 = 'inmobiliaria_app.views.server_error'
handler403 = 'inmobiliaria_app.views.permission_denied'
handler400 = 'inmobiliaria_app.views.bad_request'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name ='home'),
    path('login/', login_page, name ='login_page'),
    path('logout/', salir, name= 'salir'),
    path('register_user/', register_user, name= 'register_user'),
    path('perfil_user/', perfil_user, name= 'perfil_user'),
    path('update_user/', update_user, name= 'update_user'),
    path('delete_user/', delete_user, name= 'delete_user'),
    path('create_inm/', create_inm, name= 'create_inm'),
    path('image_add/', image_inmueble, name= 'image_inmueble'),
    path('delete_img/<int:id>/', delete_img, name= 'delete_img'),
    path('publication_inm/', publication_inm, name= 'publication_inm'),
        
    path('update_inm/', update_inm, name= 'update_inm'),
   
    path('perfil_inm/', perfil_inm, name= 'perfil_inm'),
    
    
    path('delete_inm/', delete_inm, name= 'delete_inm'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
