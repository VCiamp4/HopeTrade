from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404
from .models import Ayudante, Intercambiador, Publicacion, Filial, Categoria, Comentario
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .exceptions import edadInvalida
from django.core.exceptions import ValidationError



from django.contrib import messages
from .backends import (
    IntercambiadorBackend,
    AyudanteBackend,
    cambiar_estado_activas,
    revisar_fecha,
    
    revisar_estado,
    suspender,
    buscarIntercambiador,
    
    enviar_correo_oferta,
    obtener_intercambio,
    cambiar_inter_pendiente,
    rechazar_intercambio,
    eliminar_inter_restantes,
    tiene_ofertas, enviar_correo_acepto_intercambio, enviar_correo_rechazo_intercambio,
    enviar_correo_suspension, enviar_correo_eliminar_cuenta, enviar_intercambio_cancelado, enviar_publicacion_eliminada,
    enviar_correo_nuevo_comentario, enviar_correo_nueva_respuesta,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import PublicacionForm, IntercambiadorRegistroForm, IntercambiadorSesionForm, ComentarioForm, RespuestaForm, PublicacionModificacionForm

from .backends import IntercambiadorBackend, AyudanteBackend, revisar_fecha, revisar_estado, suspender, buscarIntercambiador, enviar_correo_oferta, enviar_correo_nuevo_comentario, enviar_correo_nueva_respuesta


from django.db.models import Q
from .models import Intercambio
from django.utils import timezone
from datetime import datetime


# Create your views here.


def nada(request):
    form_registro = IntercambiadorRegistroForm()
    form_inicio_sesion = IntercambiadorSesionForm()
    context = {
        "form_registro" : form_registro,
        "form_inicio_sesion" : form_inicio_sesion
    }
    return redirect("home")

def home(request):
    form_registro = IntercambiadorRegistroForm()
    form_inicio_sesion = IntercambiadorSesionForm()
    context = {
        "form_registro" : form_registro,
        "form_inicio_sesion" : form_inicio_sesion
    }
    return render(request, "home.html", context)

def iniciar_sesion_inter(request):
    
    if request.method == 'POST':
        diccionario = {
            'dni': request.POST["dni"],
            'contrasenia': request.POST["contrasenia"]
        }

        form_inicio_sesion = IntercambiadorSesionForm(diccionario)
        
        if form_inicio_sesion.is_valid():
            dni = form_inicio_sesion.cleaned_data['dni']
            contrasenia = form_inicio_sesion.cleaned_data['contrasenia']
            user = authenticate(request, dni=dni, password=contrasenia)
            
            if user is not None:
                if user.estado == "suspendido":
                    return render(
                        request,
                        "suspension_mensaje.html",
                        {"fecha": user.fecha_suspension, "nombre_usuario": user.nombre},
                    )
                user.backend = "registrar_intercambiador.backends.IntercambiadorBackend"
                login(request, user)
                return redirect('menu_principal')
            else:
                messages.error(request, "El DNI y/o contraseña son incorrectos")
                return redirect('home')
        else:
            for error in form_inicio_sesion.errors.values():
                messages.error(request, error)
                
            return render(request, "home.html", {"form_registro": IntercambiadorRegistroForm, "form_inicio_sesion": form_inicio_sesion})
    else:
        form_inicio_sesion = IntercambiadorSesionForm()
        
    form_registro = IntercambiadorRegistroForm()
    return render(request, "home.html", {"form_inicio_sesion": form_inicio_sesion, "form_registro": form_registro})



def iniciar_sesion_ayudante(request):
    if request.method == "GET":
        return render(request, "iniciar_sesion_ayudante.html")
    else:
        dni = request.POST["dni"]
        password = request.POST["password"]
        backend = AyudanteBackend()
        ayu = backend.authenticate(dni=dni, password=password)
        if ayu is not None:
            ayu.backend = "registrar_intercambiador.backends.AyudanteBackend"
            login(request, ayu)
            return redirect("menu_principal")
        else:
            messages.error(request, "DNI o contraseña incorrectos")
            return redirect("home")

def cerrar_sesion(request):
    logout(request)
    return redirect("home")

def inicio(request):
    return redirect("menu_principal")

@login_required
def registrar_ayu(request):
    if request.method == 'GET':
        filiales = Filial.objects.all()
        context = {
            "filiales" : filiales
        }
        return render(request, 'registrar_ayu.html', context)
    else:
        dni = request.POST['dni']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['email']
        contrasenia = request.POST['contrasenia']

        filial = Filial.objects.get(id_filial=request.POST['filial'])

        try:
            Ayudante.objects.create_user(
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasenia=contrasenia,
                filial=filial
            )
            backend = AyudanteBackend()
            ayu = backend.authenticate(dni=dni, password=contrasenia)
            ayu.backend = 'registrar_intercambiador.backends.AyudanteBackend'
            login(request, ayu)
            return redirect('menu_principal')
        except IntegrityError as e:
            error_message = str(e)
            print(error_message)
            if "UNIQUE constraint failed: registrar_intercambiador_ayudante.correo" in error_message:
                return render(request, 'registrar_ayu.html', {"error": 'El email ya está registrado en una cuenta de ayudante'})
            else:
                return render(request, 'registrar_ayu.html', {"error": 'El DNI ya está registrado en una cuenta de ayudante'})

def registrar_inter(request):
    if request.method == "POST":
        form = IntercambiadorRegistroForm(request.POST)
        if form.is_valid():
            nuevo_intercambiador = form.save(commit=False)
            nuevo_intercambiador.save()
            
            
            dni = form.cleaned_data.get('dni')
            contrasenia = form.cleaned_data.get('contrasenia')
           
            backend = IntercambiadorBackend()
            inter = backend.authenticate(request=request, dni=dni, password=contrasenia)
            if inter is not None:
                inter.backend = "registrar_intercambiador.backends.IntercambiadorBackend"
                login(request, inter)
                messages.success(request, "Bienvenido a HopeTrade")
                return redirect("menu_principal")
            else:
                messages.error(request, "Error de autenticación. Por favor, intente nuevamente.")
                return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            
            return render(request, "home.html", {"form_registro": form, "form_inicio_sesion": IntercambiadorSesionForm()})
    else:
        form = IntercambiadorRegistroForm()
    return render(request, "home.html", {"form_registro": form, "form_inicio_sesion": IntercambiadorSesionForm()}) 

@login_required
def crear_publicacion(request):
    errores = []
    exito = []

    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = request.user
            publicacion = form.save(commit=False)
            publicacion.usuario_publicacion = usuario
            publicacion.save()
            messages.success(request, "Tu publicacion fue creada con éxito")
            
            return redirect('/menu_principal/')  
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PublicacionForm()

    context = {
        'form_publicacion': form,
        'errores': errores,
        'exito': exito
    }
    return render(request, 'crear_publicacion.html', context)

@login_required
def modificar_publicacion(request): 
    categorias = Categoria.objects.all()
    filiales = Filial.objects.all()
    id_publicacion = request.POST.get("id_publicacion")

    publicacion = get_object_or_404(Publicacion, id_publicacion=id_publicacion)

    form = PublicacionModificacionForm(instance=publicacion) 

    context = {
        'form_publicacion': form,
        'publicacion': publicacion,
        'categorias':categorias,
        'filiales':filiales,
    }

    return render(request, "modificar_publicacion.html", context)

@login_required
def modifique_publicacion(request):
    if request.method == "POST":
        
        id_publicacion = request.POST.get("id_publicacion")
        publicacion = get_object_or_404(Publicacion, id_publicacion=id_publicacion)
        
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        
        if(publicacion.estado_publicacion == "activa"):
            
            if(tiene_ofertas(publicacion)):
                messages.error(request, "No podes modificar esta publicacion porque participa en una o mas ofertas. Deberas cancelar las enviadas y rechazar las recibidas")
                return redirect("menu_principal")

            if form.is_valid():
                
                if not form.cleaned_data.get('imagen_publicacion'):
                    form.cleaned_data['imagen_publicacion'] = publicacion.imagen_publicacion
                form.save()
                messages.success(request, "Se modificó la publicación con éxito.")
                return redirect('mis_publicaciones')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            messages.error(request, "Esta publicacion tiene un intercambio pendiente, para modificarla debera cancelar el intercambio")
            return redirect("menu_principal")

        
        return redirect("mi_perfil")
        #..................................
    

@login_required
def inicio_sesion_ayudante(request):
    return render(request, "inicio_sesion_ayudante.html")

@login_required
def mi_perfil(request):
    if request.method == "GET":
        usuario = request.user
        if(isinstance(usuario, Intercambiador)):
            return render(
                request,
                "mi_perfil.html",
                {
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "foto": usuario.imagen_perfil
                }
            )
        else:
            return render(
                request,
                "mi_perfil_ayudante.html",
                {
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "foto": usuario.imagen_perfil,
                },
            )
    else:
        usuario = request.user
        usuario.nombre = request.POST["nombre"]
        usuario.apellido = request.POST["apellido"]
        if 'imagenInput' in request.FILES:
            usuario.imagen_perfil = request.FILES['imagenInput']
        usuario.save()
        messages.success(request, "Cambios guardados")
        return redirect("menu_principal")

@login_required
def ver_publicacion(request):
    id_publicacion = request.POST.get("id_publicacion")
    publicacion = get_object_or_404(
        Publicacion,
        Q(estado_publicacion__iexact="activo") | Q(estado_publicacion__iexact="activa"),
        id_publicacion=id_publicacion,
    )
    usuario = request.user


    comentarios_publicacion = Comentario.objects.filter(publicacion_comentario = publicacion).order_by("-fecha_comentario")
    
    comentarios_dict = dict()
    for comentario in comentarios_publicacion:
        if comentario.es_respuesta_a_comentario is None:
            comentarios_dict[comentario] = []
        
    for comentario in comentarios_publicacion:
        if comentario.es_respuesta_a_comentario is not None:
            comentarios_dict[comentario.es_respuesta_a_comentario].append(comentario)
    
    form_nuevo_comentario = ComentarioForm()
    form_nueva_respuesta = RespuestaForm()
    context = {
        "publicacion": publicacion,
        "form_nuevo_comentario": form_nuevo_comentario,
        "form_nueva_respuesta" : form_nueva_respuesta,
        "comentarios_dict": comentarios_dict,
    }
    if(isinstance(usuario, Ayudante)):
        return render(request, "ver_publicacion_ayudante.html", context)
    else:
        return render(request, "ver_publicacion.html", context)

@login_required
def ver_mi_publicacion(request):
    # ................................................................................................................................................................................................
    publicacion = Publicacion.objects.get(id_publicacion = request.GET['id_publicacion'])
    return render(request, "ver_mi_publicacion.html", {"publicacion": publicacion})

@login_required
def suspender_cuenta(request):
    usuario = request.user
    if isinstance(usuario, Ayudante):
        if request.method == "GET":
            return render(request, "suspender_dni.html")
        else:
            usuario = buscarIntercambiador(request.POST["dni"])
            if not (usuario == None):
                if not (usuario.estado == 'suspendido'):
                    suspender(usuario)
                    enviar_correo_suspension(usuario.correo)
                    messages.success(request, "Intercambiador suspendido con exito")
                    return redirect("menu_principal")
                else:
                    return render(
                        request,
                        "suspender_dni.html",
                        {"error": "El usuario ingresado ya se encuentra suspendido"},
                    )
            else:
                return render(
                    request,
                    "suspender_dni.html",
                    {"error": "No existe intercambiador con ese dni"},
                )
    else:
        return redirect("menu_principal")
    
@login_required
def menu_principal(request):
    estados = ["activa", "Activa", "activo", "Activo"]
    usuario = request.user
    if request.method == "GET":
        categorias = Categoria.objects.all()
        filiales = Filial.objects.all()
        publicaciones = Publicacion.objects.filter(estado_publicacion__in=estados).exclude(usuario_publicacion__dni = usuario.dni)

        context = {
            "categorias": categorias,
            "filiales": filiales,
            "publicaciones": publicaciones,
        }
        if isinstance(usuario, Ayudante):
            if usuario.is_staff:
                return render(request, "menu_principal_admin.html", context)
            else:
                return render(request, "menu_principal_ayudante.html", context)
        else:
            return render(request, "menu_principal_viejo.html", context)
    else:

        categorias_seleccionadas = request.POST.getlist('categorias')
        filiales_seleccionadas = request.POST.getlist('filiales')
        
        # Si no hay categorías seleccionadas, selecciona todas las categorías
        if not categorias_seleccionadas:
            categorias_seleccionadas = Categoria.objects.all()

        # Si no hay filiales seleccionadas, selecciona todas las filiales
        if not filiales_seleccionadas:
            filiales_seleccionadas = Filial.objects.all()

        publicaciones = Publicacion.objects.filter(
            estado_publicacion__in = estados,
            categoria_publicacion__in=categorias_seleccionadas,
            filial_publicacion__in=filiales_seleccionadas
        ).exclude(usuario_publicacion__dni = usuario.dni)
        
        context = {
            'publicaciones': publicaciones,
            'categorias': Categoria.objects.all(),
            'filiales': Filial.objects.all(),
            'categorias_seleccionadas': categorias_seleccionadas,
            'filiales_seleccionadas': filiales_seleccionadas,
        }
        
        if isinstance(usuario, Ayudante):
            if usuario.is_staff:
                return render(request, "menu_principal_admin.html", context)
            else:
                return render(request, "menu_principal_ayudante.html", context)
        else:
            return render(request, "menu_principal_viejo.html", context)


@login_required
def eliminarCuentaDesdeUsuario(request):
    usuario = request.user
    publicaciones = Publicacion.objects.filter(
        usuario_publicacion=usuario
    )

    intercambios = Intercambio.objects.filter(
        Q(publi_ofertada__in=publicaciones) | Q(publi_recibida__in=publicaciones)
    )
    for i in intercambios:
        if (i.publi_recibida.usuario_publicacion == usuario):
            i.publi_ofertada.estado_publicacion = 'activa'
            i.publi_ofertada.save()
        else:
            i.publi_recibida.estado_publicacion = "activa"
            i.publi_recibida.save()
    usuario.delete()
    messages.error(request, "Cuenta eliminada exitosamente.")
    return redirect("home")

@login_required
def eliminarCuentaDesdeAyudante(request):
    if request.method == "GET":
        return render(request, "eliminar_cuenta.html")
    else:
        dni = request.POST["dni"]
        inter = buscarIntercambiador(dni)
        if not (inter == None):
            inter.delete()
            enviar_correo_eliminar_cuenta(inter.correo)
            messages.success(request, "Cuenta eliminada exitosamente.")
            return redirect("menu_principal")
        else:
            messages.error(request, "El intercambiador no existe.")
            return redirect("menu_principal")

@login_required
def realizar_oferta(request):
    if request.method == "GET":
        publi = Publicacion.objects.get(id_publicacion = request.GET["publi"])
        categoria_a_buscar = publi.categoria_publicacion
        publicaciones_cumplen_categoria = Publicacion.objects.filter(
            categoria_publicacion = categoria_a_buscar,
            usuario_publicacion = request.user
        )
        if(publicaciones_cumplen_categoria):
            publicaciones_cumplen = publicaciones_cumplen_categoria.filter(
                filial_publicacion = publi.filial_publicacion
            )
            if(publicaciones_cumplen):
                context = {
                    'publicacion_elegida' : publi,
                    'publicaciones': publicaciones_cumplen
                }
            else:
                messages.error(request, f'Para poder realizar una oferta, tenes que tener una publicacion en la filial {publi.filial_publicacion.nombre_filial}')
                return redirect('menu_principal')
        else:
            messages.error(request, f'Para poder realizar una oferta, tenes que tener una publicacion en la categoria {categoria_a_buscar.nombre_categoria}')
            return redirect('menu_principal')

        return render(request, "realizar_oferta.html", context)
    else:
        publi_recibida = Publicacion.objects.get(id_publicacion=request.POST["id_publicacion_elegida"])
        publi_a_ofertar = Publicacion.objects.get(id_publicacion = request.POST["id_publicacion"])
        if (publi_a_ofertar.estado_publicacion == 'pendiente'):
            messages.error(request, "Esta publicación está en trámite de intercambio, no se puede realizar ofertas")
            return redirect('menu_principal')
        else:
            publi_a_ofertar.save()
            fecha = request.POST["fecha"]
            hora = request.POST["hora"]
            fecha_hora_oferta = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if(revisar_fecha(fecha_hora_oferta)):
                intercambio = Intercambio(
                    fecha_concretada=fecha_hora_oferta,
                    fecha_oferta=timezone.now(),
                    estado="ofertado", 
                    publi_ofertada=publi_a_ofertar,
                    publi_recibida=publi_recibida,
                    filial=publi_recibida.filial_publicacion
                )
                intercambio.save()
                correo_publicacion_elegida = publi_recibida.usuario_publicacion.correo
                titulo_publicacion_elegida = publi_recibida.titulo_publicacion
                enviar_correo_oferta(correo_publicacion_elegida, titulo_publicacion_elegida)
                messages.success(request, 'Tu publicacion fue ofertada con exito')
                return redirect('menu_principal')
            else:
                messages.error(request, "Esta fecha no es valida")
                return redirect('menu_principal')

@login_required
def ver_mis_publicaciones(request):
    usuario = request.user
    publicaciones = Publicacion.objects.filter(usuario_publicacion = usuario)
    context = {
        "publicaciones" : publicaciones
    }
    return render(request, 'ver_mis_publicaciones.html', context)

@login_required
def listar_intercambios_dia(request):
    if request.method == "GET":
        usuario = request.user
        fecha_hoy = timezone.now().date()
        intercambios_del_dia = Intercambio.objects.filter(filial=usuario.filial, fecha_concretada__date = fecha_hoy, estado = 'pendiente').order_by('fecha_concretada')
        context = {
            "intercambios" : intercambios_del_dia
        }
        return render(request, "listar_intercambios_dia.html", context)
    else:
            id_intercambio = request.POST.get('id_intercambio')
            accion = request.POST.get('action')
            intercambio = Intercambio.objects.get(id_intercambio=id_intercambio)

            if accion == "confirmar":
                intercambio.estado = "realizado"
                intercambio.fecha_concretada = timezone.now()
                intercambio.publi_ofertada.estado_publicacion = "intercambiada"
                intercambio.publi_recibida.estado_publicacion = "intercambiada"
                intercambio.publi_ofertada.save()
                intercambio.publi_recibida.save()
                intercambio.save()
                messages.success(request, 'Intercambio confirmado con éxito.')
            elif accion == "cancelar":
                motivo = request.POST["motivo_cancelacion"]
                intercambio.estado = "cancelado"
                intercambio.razon_cancelacion = motivo
                intercambio.save()
                messages.success(request, 'Intercambio cancelado con éxito.')
            return redirect(menu_principal)

@login_required
def eliminar_publicacion(request):
    id = request.POST.get("id_publicacion") if  request.POST.get("id_publicacion") != None else  request.POST.get("id_publicacion2")
    publicacion = Publicacion.objects.get(id_publicacion = id)
    if(publicacion.estado_publicacion == 'pendiente'):
        messages.error(request, "No se puede eliminar una publicación en estado pendiente de intercambio, primero debe cancelar el intercambio")
    else:
        cambiar_estado_activas(publicacion)
        publicacion.delete()
        if(isinstance(request.user, Ayudante)):
            enviar_publicacion_eliminada(publicacion.usuario_publicacion.correo, publicacion.titulo_publicacion)
        messages.success(request, "Su publicacion fue eliminada con exito")
    return redirect('menu_principal')

@login_required
def listar_mis_intercambios(request):
    usuario = request.user
    if request.method == 'GET':
        intercambios = Intercambio.objects.filter(Q(publi_recibida__usuario_publicacion = usuario) | Q(publi_ofertada__usuario_publicacion = usuario), estado__in = ['pendiente', 'realizado'])
        context = {
            'intercambios' : intercambios
        }
        return render(request, 'mis_intercambios.html', context)
    else:
        intercambio = Intercambio.objects.get(id_intercambio = request.POST['id_intercambio'])
        rechazar_intercambio(intercambio)
        if(intercambio.publi_ofertada.usuario_publicacion == usuario):
            destinatario = intercambio.publi_recibida.usuario_publicacion.correo
            titulo_publicacion = intercambio.publi_recibida.titulo_publicacion
        else:
            destinatario = intercambio.publi_ofertada.usuario_publicacion.correo
            titulo_publicacion = intercambio.publi_ofertada.titulo_publicacion
        enviar_intercambio_cancelado(destinatario, titulo_publicacion)
        messages.success(request, "Intercambio cancelado con éxito.")
        return redirect('menu_principal')

@login_required
def listar_ofertas_propuestas(request):
    if request.method == "GET":
        intercambios = Intercambio.objects.filter(
            publi_recibida__id_publicacion = request.GET["id_publicacion_recibida"],
            estado='ofertado'
        )

        publi_recibe = Publicacion.objects.get(id_publicacion=request.GET["id_publicacion_recibida"])

        # Obtener las IDs de las publicaciones recibidas de estos intercambios
        publi_ofertada_ids = intercambios.values_list('publi_ofertada_id', flat=True)

        # Obtener las publicaciones que coinciden con estas IDs
        publicaciones = Publicacion.objects.filter(id_publicacion__in=publi_ofertada_ids)
        if publicaciones:
            context = {
                'publicaciones': publicaciones,
                'publi_recibe': publi_recibe
            }

            return render(request, "listar_ofertas_propuestas.html", context)
        else:
            messages.error(request, "Aún no ha recibido ofertas de intercambio para esta publicación.")
            return redirect('mis_publicaciones')
    else:
        accion = request.POST.get('action')
        id_publicacion_recibida = request.POST["id_publicacion_recibida"]
        id_publicacion_ofertada = request.POST["id_publicacion_ofertada"]
        publi_que_oferto = Publicacion.objects.get(
            id_publicacion=id_publicacion_ofertada
        )
        publi_que_recibio = Publicacion.objects.get(
            id_publicacion=id_publicacion_recibida
        )
        intercambio = obtener_intercambio(id_publicacion_recibida, id_publicacion_ofertada)
        if(accion == 'aceptar'):
            cambiar_inter_pendiente(intercambio)
            eliminar_inter_restantes(id_publicacion_recibida, id_publicacion_ofertada)
            filial = intercambio.filial
            fecha = intercambio.fecha_concretada
            messages.success(request, f"Felicitaciones, se ha notificado de tu aceptación al intercambiador. Las ofertas relacionadas con esta publicacion se dieron de baja. Recuerda que se requiere tu presencialidad en la filial {filial} el dia {fecha}")
            enviar_correo_acepto_intercambio(publi_que_oferto.usuario_publicacion, publi_que_recibio.titulo_publicacion)
            return redirect('menu_principal')
        else:
            rechazar_intercambio(intercambio)
            enviar_correo_rechazo_intercambio(publi_que_oferto.usuario_publicacion, publi_que_recibio.titulo_publicacion, publi_que_oferto.titulo_publicacion)
            messages.success(request, "La oferta fue rechazada con éxito.")
            return redirect("menu_principal")

@login_required
def listar_mis_ofertas_pendientes(request):
    if request.method == 'GET':
        usuario = request.user
        intercambios = Intercambio.objects.filter(publi_ofertada__usuario_publicacion=usuario, estado = 'ofertado')
        context = {
            'intercambios' : intercambios
        }
        return render(request, 'mis_ofertas_pendientes.html', context)
    else:
        intercambio = Intercambio.objects.get(id_intercambio = request.POST['id_intercambio'])
        intercambio.publi_ofertada.estado_publicacion = 'activa'
        intercambio.publi_ofertada.save()
        intercambio.delete()
        messages.success(request, 'Se ha cancelado la oferta efectivamente')
        return redirect('menu_principal')

@login_required
def comentar_en_publicacion(request):
    if request.method == "POST":
        
        id_publicacion = request.POST.get("id_publicacion")
        publicacion = get_object_or_404(Publicacion, id_publicacion=id_publicacion)
        
        # Verificar si se está respondiendo a un comentario existente
        if 'comentario_a_responder' in request.POST:
            id_comentario_padre = request.POST.get('comentario_a_responder')
            comentario_padre = get_object_or_404(Comentario, id_comentario=id_comentario_padre)
            form = RespuestaForm(request.POST)
        else:
            form = ComentarioForm(request.POST)
    
        if form.is_valid():
            usuario = request.user
            comentario = form.save(commit=False)
            comentario.usuario_comentario = request.user
            comentario.publicacion_comentario = publicacion
            
            if 'comentario_a_responder' in request.POST:
                comentario.es_respuesta_a_comentario = comentario_padre
                respuesta = form.cleaned_data.get("texto_comentario")
                
            comentario.save()

            if 'comentario_a_responder' in request.POST:
                correo_duenio_comentario = comentario_padre.usuario_comentario.correo
                titulo_publicacion = publicacion.titulo_publicacion
                enviar_correo_nueva_respuesta(correo_duenio_comentario, titulo_publicacion, respuesta)
                messages.success(request, "Tu respuesta fue añadida")
                

            else:
                correo_duenio_publicacion = publicacion.usuario_publicacion.correo
                titulo_publicacion_elegida = publicacion.titulo_publicacion
                nombre = request.user.get_nombre_completo_usuario()
                enviar_correo_nuevo_comentario(correo_duenio_publicacion, titulo_publicacion_elegida, nombre)
                messages.success(request, "Tu comentario ha sido añadido")
        else:
            for error in form.errors.values():    
                messages.error(request, error)
                
    return redirect("menu_principal")

@login_required
def eliminar_comentario(request):
    if (request.method == "POST"):
        #id_publicacion = request.POST["id_publicacion"]
        id_comentario = request.POST["id_comentario"]
        comentario = Comentario.objects.get(id_comentario = id_comentario)
        comentario.delete()
        messages.success(request, "Su comentario ha sido eliminado")
       #publicacion = Publicacion.objects.get(id_publicacion = id_publicacion)
        #mis_comentarios = Comentario.objects.filter(usuario_comentario = request.user, publicacion_comentario = publicacion)
        #comentarios_publicacion = Comentario.objects.filter(publicacion_comentario = publicacion).exclude(usuario_comentario = request.user)
        #form_nuevo_comentario = ComentarioForm()
        #context = {
        #    "publicacion" : publicacion,
        #    "form_nuevo_comentario" : form_nuevo_comentario,
        #    "mis_comentarios" : mis_comentarios,
        #    "comentarios_publicacion" : comentarios_publicacion,
#
        #}
        #return render(request, "ver_publicacion.html", context)
        return redirect('menu_principal')

def listar_comentarios(request):
    if request.method == "POST":
        id_publicacion = request.POST["id_publicacion"]
        publicacion = get_object_or_404(Publicacion, id_publicacion=id_publicacion)
        # el guión de ahi NO se borra. Saludos
        comentarios_publicacion = Comentario.objects.filter(publicacion_comentario = publicacion).order_by("-fecha_comentario")
        
        comentarios_dict = dict()

        for comentario in comentarios_publicacion:

            if comentario.es_respuesta_a_comentario is None:
                comentarios_dict[comentario] = []
            
        for comentario in comentarios_publicacion:
            if comentario.es_respuesta_a_comentario is not None:
                comentarios_dict[comentario.es_respuesta_a_comentario].append(comentario)

        context = {
            "publicacion" : publicacion,
            "comentarios_dict" : comentarios_dict,
            "form_nuevo_comentario" : RespuestaForm()
        }
        return render(request, "listar_comentarios.html", context)

