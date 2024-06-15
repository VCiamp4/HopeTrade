from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .exceptions import edadInvalida
from .metodosComunes import verificar_edad

# Create your models here.

class IntercambiadorManager(BaseUserManager):
    def create_user(self, dni, nombre, apellido, correo, fecha_nacimiento, contrasenia=None, **extra_fields):
        email = self.normalize_email(correo)
        if (verificar_edad(fecha_nacimiento)):
            #si la edad es mayor a 18 (y menor a 100 para que no pongan cualquier fecha)
            if not(Intercambiador.objects.filter(dni=dni).exists()): #si no existe uno con el mismo dni
                user = self.model(
                    dni=dni, nombre=nombre, apellido=apellido, correo=email, fecha_nacimiento=fecha_nacimiento, **extra_fields
                )
                user.username = dni
                user.set_password(contrasenia)
                user.save()
                return user
            else: #sino levanta error de integridad.
                raise IntegrityError
        else:
            raise edadInvalida('mensajedeerror')

    def create_superuser(
        self, dni, nombre, apellido, correo, contrasenia=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            dni, nombre, apellido, correo, contrasenia, **extra_fields
        )
    
    def get_user(self, user_id):
        try:
            return self.get(pk=user_id)
        except self.model.DoesNotExist:
            return None


class Intercambiador(AbstractBaseUser, BaseUserManager):

    opciones_estado = (('suspendido', 'Suspendido'), ('activo', 'Activo'))

    dni = models.PositiveIntegerField(primary_key=True, editable=True, unique=True)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    correo = models.EmailField(unique=True)
    contrasenia = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(choices=opciones_estado, default='activo', max_length=15)
    fecha_suspension = models.DateTimeField(null=True, blank=True, default=None)
    imagen_perfil = models.ImageField(upload_to="fotos/", default="perfil_default.jpg")

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="intercambiador_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="intercambiador_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = IntercambiadorManager()

    USERNAME_FIELD = 'dni'

    def __str__(self):
        texto = "Intercambiador con DNI:{0}"
        return texto.format(self.dni)
    def get_nombre_completo_usuario(self):
        return "{} {}".format(self.nombre, self.apellido)


class AyudanteManager(BaseUserManager):
    def create_user(self, dni, nombre, apellido, correo, filial, contrasenia=None, **extra_fields):
        email = self.normalize_email(correo)
        if not(Ayudante.objects.filter(dni=dni).exists()): #si no existe uno con el mismo dni
            user = self.model(
                dni=dni, nombre=nombre, apellido=apellido, correo=email, filial=filial, **extra_fields
            )    
            user.set_password(contrasenia)
            user.save()
            return user
        else: #sino levanta error de integridad.
            raise IntegrityError

    def create_superuser(
        self, dni, nombre, apellido, correo, contrasenia=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            dni, nombre, apellido, correo, contrasenia, **extra_fields
        )
    
    def get_user(self, user_id):
        try:
            return self.get(pk=user_id)
        except self.model.DoesNotExist:
            return None
    

class Filial(models.Model):
    id_filial = models.AutoField(primary_key=True, editable=False, unique=True)
    nombre_filial = models.CharField(max_length=50)
    direccion_filial = models.CharField(max_length=100)

    def __str__(self):
        return "Filial " + self.nombre_filial + " - Dirección " + self.direccion_filial


class Ayudante(AbstractBaseUser, PermissionsMixin):

    dni = models.PositiveIntegerField(primary_key=True, editable=False, unique=True)
    nombre = models.CharField(max_length=15)
    apellido = models.CharField(max_length=15)
    correo = models.EmailField(max_length=15, unique=True)
    contrasenia = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, null=True, blank=True)
    imagen_perfil = models.ImageField(upload_to="fotos/", default="perfil_default.jpg")

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="ayudante_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="ayudante_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = AyudanteManager()

    USERNAME_FIELD = 'dni'

    def __str__(self):
        texto = "Ayudante con DNI:{0}"
        return texto.format(self.dni)


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, editable=False, unique=True)
    nombre_categoria = models.CharField(max_length=25, editable=True, unique=True)

    def __str__(self):
        return self.nombre_categoria


class Publicacion(models.Model):

    opciones = (
        ("activa", "Activa"),
        ("pendiente", "Pendiente"),
        ("intercambiada", "Intercambiada")
    )

    id_publicacion = models.AutoField(primary_key=True, editable=False, unique=True)
    titulo_publicacion = models.CharField(max_length=30, editable=True)
    descripcion_publicacion = models.CharField(max_length=280, editable=True)
    filial_publicacion = models.ForeignKey(Filial, on_delete=models.CASCADE)
    categoria_publicacion = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_publicacion = models.ImageField(
        upload_to="media/fotos",
        default="../static/logo.png",
    )
    usuario_publicacion = models.ForeignKey(
        Intercambiador, on_delete=models.CASCADE, null=True, blank=True
    )


    estado_publicacion = models.CharField(choices=opciones, default="activa", max_length=15)

    


class Comentario(models.Model):

    # .............................Campos de comentario.......................
    id_comentario = models.AutoField(primary_key=True, editable=False, unique=True)

    publicacion_comentario = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comments')
    usuario_comentario = models.ForeignKey(Intercambiador, on_delete=models.CASCADE)
    es_respuesta_a_comentario = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    texto_comentario = models.CharField(max_length=280)
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    # .............................Campos de comentario.......................

    # --------------------------------Métodos de comentario ----------------------------
    class Meta:
        ordering = ['fecha_comentario']

    def __str__(self):
        if (self.es_respuesta_a_comentario):
            texto = "El autor de la publicación respondió {0}"
            return texto.format(self.texto_comentario)
        
        return self.texto_comentario
    

class Intercambio(models.Model):
    opciones = (
        ("ofertado", "Ofertado"),
        ("pendiente", "Pendiente"),
        ("cancelado", "Cancelado"),
        ("realizado", "Realizado")
    )

    id_intercambio = models.AutoField(primary_key=True, editable=False, unique=True)
    fecha_concretada = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    fecha_oferta = models.DateTimeField(auto_now=False, auto_now_add=False)
    estado = models.CharField(choices=opciones, default="ofertado", max_length=20)
    publi_ofertada = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="ofertada_intercambio")
    publi_recibida = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="recibida_intercambio")
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    razon_cancelacion = models.CharField(default="", max_length=280)