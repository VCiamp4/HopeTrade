"""
URL configuration for hopetrade project.

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
from django.contrib import admin
from django.urls import path
from registrar_intercambiador import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.nada, name="nada"),
    path("home/", views.home, name="home"),
    path("registrar_ayu/", views.registrar_ayu),
    path("menu_principal/", views.menu_principal, name="menu_principal"),
    path("signup_inter/", views.registrar_inter, name="registrar_intercambiador"),
    path("signin_inter/", views.iniciar_sesion_inter, name="iniciar_sesion_intercambiador"),
    path("signin_ayu/", views.iniciar_sesion_ayudante, name="iniciar_sesion_ayudante"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("mi_perfil/", views.mi_perfil, name="mi_perfil"),
    path("crear_publicacion/", views.crear_publicacion, name="crear_publicacion"),
    path("inicio/", views.inicio, name="inicio"),
    path("ver_publicacion/", views.ver_publicacion, name="ver_publicacion"),
    path("suspender_cuenta/", views.suspender_cuenta, name="suspender_cuenta"),
    path("eliminarCuentaDesdeUsuario/", views.eliminarCuentaDesdeUsuario, name="eliminarCuentaDesdeUsuario"),
    path("eliminarCuentaDesdeAyu/", views.eliminarCuentaDesdeAyudante, name="eliminarCuentaDesdeAyudante"),
    path("modificar_publicacion/", views.modificar_publicacion, name="modificar_publicacion"),
    path("modifique_publicacion/", views.modifique_publicacion, name="modifique_publicacion"),
    path("realizar_oferta/", views.realizar_oferta, name="realizar_oferta"),
    path("mis_publicaciones/", views.ver_mis_publicaciones, name="mis_publicaciones"),
    path("listar_intercambios_dia/", views.listar_intercambios_dia, name="listar_intercambios_dia"),
    path("ver_mi_publicacion/", views.ver_mi_publicacion, name="ver_mi_publicacion"),
    path("eliminar_publicacion/", views.eliminar_publicacion, name="eliminar_publicacion"),
    path("listar_mis_intercambios/", views.listar_mis_intercambios, name="listar_mis_intercambios"),
    path("listar_ofertas_propuestas/", views.listar_ofertas_propuestas, name="listar_ofertas_propuestas"),
    path("listar_mis_ofertas_pendientes/", views.listar_mis_ofertas_pendientes, name="listar_mis_ofertas_pendientes"),
    path("comentar_en_publicacion/", views.comentar_en_publicacion, name="comentar_en_publicacion"),
    path("eliminar_comentario/", views.eliminar_comentario, name="eliminar_comentario"),
    path("listar_comentarios/", views.listar_comentarios, name="listar_comentarios"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
