from django.db import IntegrityError, transaction

from app.modelo.usuario import Usuario


class UsuarioDuplicado(Exception):
    """El correo o el DNI ya están registrados."""


class UsuarioDAO:
    @staticmethod
    def guardar(usuario: Usuario) -> Usuario:
        try:
            with transaction.atomic():
                usuario.save()
        except IntegrityError as e:
            raise UsuarioDuplicado() from e
        return usuario

    @staticmethod
    def buscar_por_email(email: str):
        return Usuario.objects.filter(email=email).first()

    @staticmethod
    def buscar_por_id(id_usuario: int):
        return Usuario.objects.filter(pk=id_usuario).first()