from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class Usuario(AbstractBaseUser):
    """Entidad Usuario. Hereda de AbstractBaseUser, que ya aporta
    password (con hash), last_login, set_password() y check_password()."""

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=120, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombres", "apellidos", "dni", "telefono"]

    objects = BaseUserManager()

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"