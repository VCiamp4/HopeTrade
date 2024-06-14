from django.contrib.auth.hashers import check_password
from .models import Intercambiador, Publicacion, Categoria, Filial, Ayudante, Intercambio
from django.contrib.auth.backends import BaseBackend
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
from datetime import datetime
from django.db.models import Q

def autenticarIntercambiador(dni, password):
    try:
        user = Intercambiador.objects.get(dni=dni)
        print("Lo encontre")
        if user.check_password(password):

            return user
    except Intercambiador.DoesNotExist:
        return None


def autenticarAyudante(dni, password):
    try:
        user = Ayudante.objects.get(dni=dni)
        if user.check_password(password):
            return user
    except Ayudante.DoesNotExist:
        return None


def buscarIntercambiador(dni):
    try:
        user = Intercambiador.objects.get(dni=dni)
        return user
    except Intercambiador.DoesNotExist:
        return None


def revisar_estado(usuario):
    if usuario.estado == "suspendido":
        if usuario.fecha_suspension.replace(tzinfo=None) <= datetime.now().replace(
            tzinfo=None
        ):
            usuario.estado = "activo"
            usuario.fecha_suspension = None
            usuario.save()
            return True
        else:
            return False
    else:
        return True


def suspender(usuario):
    usuario.estado = "suspendido"
    usuario.fecha_suspension = datetime.now() + timedelta(days=5)
    usuario.save()


class IntercambiadorBackend(BaseBackend):

    def authenticate(self, request, dni=None, password=None, **kwargs):
        try:
            user = Intercambiador.objects.get(dni=dni, contrasenia=password)
            return user
        except Intercambiador.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Intercambiador.objects.get(pk=user_id)
        except Intercambiador.DoesNotExist:
            return None


class AyudanteBackend(BaseBackend):
    def authenticate(self, dni=None, password=None):
        return autenticarAyudante(dni, password)

    def get_user(self, user_id):
        try:
            return Ayudante.objects.get(pk=user_id)
        except Ayudante.DoesNotExist:
            return None


def autenticarAyudante(dni, password):
    try:
        user = Ayudante.objects.get(dni=dni)
        if user.check_password(password):
            return user
    except Ayudante.DoesNotExist:
        return None





def enviar_correo(destinatario, asunto, cuerpo):
    remitente = "hopetradeteam@gmail.com" 
    contraseña = "yjiq vgzi vbzz tdre"

    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        return True
    except Exception as e:
        raise e

def enviar_correo_oferta(destinatario, titulo_publicacion):
    asunto = "Usted tiene una oferta nueva"
    cuerpo = f"Hola! Alguien realizo una oferta por la publicacion con titulo: {titulo_publicacion} que tiene activa en Hope Trade, por favor revise la lista de ofertas pendientes de la publicacion"
    enviar_correo(destinatario, asunto, cuerpo)

def enviar_correo_acepto_intercambio(destinatario, titulo_publicacion):
    asunto = "Alguien acepto su oferta"
    cuerpo = f"Hola! Su oferta por la publicacion: {titulo_publicacion} que realizo en Hope Trade fue aceptada por favor revise la lista de intercambios pendientes"
    enviar_correo(destinatario.correo, asunto, cuerpo)



def enviar_correo_rechazo_intercambio(destinatario, titulo_publicacion_recibio, titulo_publicacion_oferto):
    asunto = "Alguien rechazo su oferta"
    cuerpo = f"Hola! Su oferta por la publicacion: {titulo_publicacion_recibio} que realizo en Hope Trade fue rechazada, su publicacion con titulo {titulo_publicacion_oferto} fue devuelta a estado activa"
    enviar_correo(destinatario.correo, asunto, cuerpo)

def enviar_correo_suspension(destinatario):
    mensaje = "Hola, le informamos que su cuenta de HopeTrade fue suspendida."
    asunto = "Suspension de cuenta"
    enviar_correo(destinatario, asunto, mensaje)


def enviar_correo_eliminar_cuenta(destinatario):
    mensaje = "Hola, le informamos que su cuenta de HopeTrade fue eliminada."
    asunto = "Suspension de cuenta"
    enviar_correo(destinatario, asunto, mensaje)


def enviar_intercambio_cancelado(destinatario, titulo_publicacion):
    mensaje = f"Hola, le informamos que el intercambio pendiente que incluye a su publicacion con titulo: {titulo_publicacion} fue cancelado. Su publicacion se devolvio a estado activa."
    asunto = "Intercambio cancelado"
    enviar_correo(destinatario, asunto, mensaje)


def enviar_publicacion_eliminada(destinatario, titulo_publicacion):
    mensaje = f"Hola, le informamos que su publicacion con titulo: {titulo_publicacion} fue eliminada por la administracion de HopeTrade."
    asunto = "Publicacion eliminada"
    enviar_correo(destinatario, asunto, mensaje)


def enviar_correo_nuevo_comentario(destinatario, titulo_publicacion, nombre_comentador):
    asunto = "Tienes un nuevo comentario"
    cuerpo = f"Hola! {nombre_comentador} realizó un comentario en la publicación con título: {titulo_publicacion} que tenes activa en HopeTrade, por favor revisa tu publicación para responderle"
    enviar_correo(destinatario, asunto, cuerpo)

def enviar_correo_nueva_respuesta(destinatario, titulo_publicacion, respuesta):
    asunto = f"Te respondieron en {titulo_publicacion}"
    cuerpo = f"Hola! El/la dueño/a de la publicación {titulo_publicacion} en la que comentaste te respondió: {respuesta}. Andá a HopeTrade para más información"
    enviar_correo(destinatario, asunto, cuerpo)


def revisar_fecha(fecha):
    if fecha.date() < datetime.now().date():
        return False
    if fecha.weekday() == 6:
        return False
    if fecha.hour < 8 or fecha.hour >= 20:
        return False
    return True


def cambiar_estado_activas(publicacion):
    intercambios = Intercambio.objects.filter(publi_recibida = publicacion)
    for i in intercambios:
        p = i.publi_ofertada
        p.estado_publicacion = 'activa'
        p.save()
    return True

def obtener_intercambio(publi_recibida_id, publi_ofertada_id):
    return get_object_or_404(
        Intercambio,
        publi_recibida__id_publicacion=publi_recibida_id,
        publi_ofertada__id_publicacion=publi_ofertada_id
    )

def cambiar_inter_pendiente(intercambio):
    intercambio.estado = 'pendiente'
    intercambio.publi_recibida.estado_publicacion = 'pendiente'
    intercambio.publi_ofertada.estado_publicacion = 'pendiente'
    intercambio.publi_recibida.save()
    intercambio.publi_ofertada.save()
    intercambio.save()


def rechazar_intercambio(intercambio):
    intercambio.publi_recibida.estado_publicacion = "activa"
    intercambio.publi_ofertada.estado_publicacion = "activa"
    intercambio.publi_recibida.save()
    intercambio.publi_ofertada.save()
    intercambio.delete()

def eliminar_inter_restantes(id_publicacion_recibida, id_publicacion_ofertada):
    intercambios_restantes1 = Intercambio.objects.filter(
                publi_recibida__id_publicacion = id_publicacion_recibida
            ).exclude(publi_ofertada__id_publicacion = id_publicacion_ofertada)

    intercambios_restantes2 = Intercambio.objects.filter(
        publi_ofertada__id_publicacion = id_publicacion_recibida
    )

    for i in intercambios_restantes2:
        i.delete()    
    
    for i in intercambios_restantes1:
        i.publi_ofertada.estado_publicacion = 'activa'
        i.publi_ofertada.save()
        i.delete()

def tiene_ofertas(publicacion):
    intercambios = Intercambio.objects.filter(Q(publi_recibida = publicacion) | Q(publi_ofertada = publicacion))
    if(intercambios):
        return True
    else:
        return False

