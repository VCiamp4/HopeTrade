# forms.py
from django import forms
from .models import Publicacion, Comentario, Intercambiador
from .metodosComunes import verificar_edad
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import datetime


class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'titulo_publicacion', 
            'descripcion_publicacion', 
            'filial_publicacion', 
            'categoria_publicacion', 
            'imagen_publicacion'
        ]
        widgets = {
            'titulo_publicacion': forms.TextInput(attrs={
                'id': 'titulo_publicacion',
                'name': 'titulo_publicacion',
                'maxlength': 30,
                'minlength': 4,
                'placeholder': 'Título',
                'required': True,
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px;'
            }),
            'descripcion_publicacion': forms.Textarea(attrs={
                'id': 'descripcion_publicacion',
                'placeholder': 'Descripción...',
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px; resize: none; height: 150px;'
            }),
            'filial_publicacion': forms.Select(attrs={
                'id': 'filial_publicacion',
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px; font-size: 16px;',
                'required': True
            }),
            'categoria_publicacion': forms.Select(attrs={
                'id': 'categoria_publicacion',
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px; font-size: 16px;',
                'required': True
            }),
            'imagen_publicacion': forms.ClearableFileInput(attrs={
                'id': 'imagenInput',
                'class': 'form-control-file',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PublicacionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['imagen_publicacion'].required = False

    def clean_titulo_publicacion(self):
        titulo = self.cleaned_data.get('titulo_publicacion')
        if len(titulo) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres.')
        
        if Publicacion.objects.filter(titulo_publicacion=titulo).exclude(id_publicacion=self.instance.id_publicacion).exists():
            raise forms.ValidationError('El título ya está en uso')
        return titulo

class PublicacionModificacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'titulo_publicacion', 
            'descripcion_publicacion', 
            'filial_publicacion', 
            'categoria_publicacion', 
            'imagen_publicacion'
        ]
        widgets = {
            'titulo_publicacion': forms.TextInput(attrs={
                'id': 'titulo_publicacion',
                'name': 'titulo_publicacion',
                'maxlength': 30,
                'minlength': 4,
                'placeholder': 'Título',
                'required': True,
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px;'
            }),
            'descripcion_publicacion': forms.Textarea(attrs={
                'id': 'descripcion_publicacion',
                'placeholder': 'Descripción...',
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px; resize: none; height: 150px;'
            }),
            'filial_publicacion': forms.Select(attrs={
                'id': 'filial_publicacion',
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px; font-size: 16px;',
                'required': True
            }),
            'categoria_publicacion': forms.Select(attrs={
                'id': 'categoria_publicacion',
                'style': 'width: calc(100% - 22px); padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px; font-size: 16px;',
                'required': True
            }),
            'imagen_publicacion': forms.ClearableFileInput(attrs={
                'id': 'imagenInput',
                'class': 'form-control-file',
                'required': False
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PublicacionModificacionForm, self).__init__(*args, **kwargs)

    def clean_titulo_publicacion(self):
        titulo = self.cleaned_data.get('titulo_publicacion')
        if len(titulo) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres.')
        
        if Publicacion.objects.filter(titulo_publicacion=titulo).exclude(id_publicacion=self.instance.id_publicacion).exists():
            raise forms.ValidationError('El título ya está en uso')
        return titulo


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'texto_comentario'
        ]
        labels = {
            'texto_comentario' : "Nuevo Comentario"
        }
        widgets = {
            'texto_comentario': forms.Textarea(attrs={
            'id': 'texto_comentario',
            'placeholder': 'Ingrese un comentario',
            'style': 'width: 100%; font-size: 1.25rem; padding: 5px; box-sizing: border-box; resize: none; height: 100px;',
            'maxlength': "280"
            }),
        }
    
    def clean_texto_comentario(self):
        texto = self.cleaned_data.get('texto_comentario')
        if len(texto) < 5:
            raise forms.ValidationError('El comentario debe tener al menos 5 caracteres.')
        return texto

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto_comentario']
        labels = {
            'texto_comentario' : "Responder comentario"
        }
        widgets = {
            'texto_comentario': forms.Textarea(attrs={
                'id': 'texto_comentario',
                'placeholder': 'Ingrese un comentario',
                'style': 'width: 100%; font-size: 1.25rem; padding: 10px; box-sizing: border-box; resize: none; height: 50px;',
                'maxlength' : "280"
            }),
        }
        
        def clean_texto_comentario(self):
            texto = self.cleaned_data.get('texto_comentario')
            if len(texto) < 5:
                
                raise forms.ValidationError('El comentario debe tener al menos 5 caracteres.')
            return texto


class IntercambiadorRegistroForm(forms.ModelForm):
    class Meta:
        model = Intercambiador
        fields = [
            'dni',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'correo',
            'contrasenia'
        ]

        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'dni_nuevo_intercambiador',
                'name': 'dni_nuevo_intercambiador',
                'maxlength': 9,
                'placeholder': 'DNI',
                'required': True,
                'pattern': '\d*',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '')",
                'style': 'font-size: 1.0rem; width: 100%; margin-bottom: 5px; padding: 1px;'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'nombre_nuevo_intercambiador',
                'name': 'nombre_nuevo_intercambiador',
                'placeholder': 'Nombre',
                'required': True,
                'maxlength': 25,
                'pattern': '[A-Za-z\s]+',
                'oninput': "this.value = this.value.replace(/[^A-Za-z\s]/g, '')",
                'style': 'font-size: 1.0rem; width: 100%; margin-bottom: 5px; padding: 1px;'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'apellido_nuevo_intercambiador',
                'name': 'apellido_nuevo_intercambiador',
                'placeholder': 'Apellido',
                'required': True,
                'maxlength': 25,
                'pattern': '[A-Za-z\s]+',
                'oninput': "this.value = this.value.replace(/[^A-Za-z\s]/g, '')",
                'style': 'font-size: 1.0rem; width: 100%; margin-bottom: 5px; padding: 1px;'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'correo',
                'name': 'correo',
                'placeholder': 'Correo electrónico',
                'required': True,
                'style': 'font-size: 1.0rem; width: 100%; margin-bottom: 5px; padding: 1px;'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'fecha_nacimiento',
                'name': 'fecha_nacimiento',
                'required': True,
                'type': 'date',
                'style': 'font-size: 1.0rem; width: 100%; margin-bottom: 5px; padding: 1px;'
            }),
            'contrasenia': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'contrasenia',
                'name': 'contrasenia',
                'placeholder': 'Contraseña',
                'maxlength': 30,
                'required': True,
                'style': 'font-size: 1.0rem; width: 100%; margin-bottom: 5px; padding: 1px;'
            }),
        }

        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo Electrónico',
            'contrasenia': 'Contraseña',
            'fecha_nacimiento': 'Fecha de Nacimiento',
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Intercambiador.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe un usuario con ese DNI.")
        return dni

    def verificar_edad(self, fecha_nacimiento):
        # Función para verificar si el usuario es mayor de edad
        today = datetime.now()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        return age >= 18

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not self.verificar_edad(fecha):
            raise forms.ValidationError("Usted es menor de edad, no puede usar el sitio.")
        return fecha

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Intercambiador.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo electrónico.")
        return correo

    



class IntercambiadorSesionForm(forms.ModelForm):
    class Meta:
        model = Intercambiador
        fields = ["dni", "contrasenia"]
        labels = {"dni": "DNI", "contrasenia": "Contraseña"}
        widgets = {
            "dni": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "dni_sesion_intercambiador",
                    "name": "dni",
                    "maxlength": 9,
                    "placeholder": "DNI",
                    "required": True,
                    "pattern": "\d*",
                    "oninput": "this.value = this.value.replace(/[^0-9]/g, '')",
                    "style": "font-size:1.0rem; padding:1px ",
                }
            ),
            "contrasenia": forms.PasswordInput(
                {
                    "class": "form-control",
                    "name": "contrasenia",
                    "maxlength" : 30,
                    "placeholder": "Contraseña",
                    "required": True,
                    "style": "font-size:1.0rem; padding:1px",
                }
            ),
        }

    def clean(self):
        
        dni = self.cleaned_data.get('dni')
        contrasenia = self.cleaned_data.get('contrasenia')
        
        if dni and contrasenia:
            try:
                user = Intercambiador.objects.get(dni=dni)

                if user.contrasenia != contrasenia:

                    raise forms.ValidationError("El DNI y/o contraseña son incorrectos")
            except Intercambiador.DoesNotExist:
                
                raise forms.ValidationError("El DNI y/o contraseña son incorrectos")

        return {'dni': dni , 'contrasenia':contrasenia}
