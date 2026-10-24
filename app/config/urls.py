from django.urls import path

from app.controlador import usuarioController as c

urlpatterns = [
    path("", c.login_vista, name="login"),
    path("registro/", c.registro_vista, name="registro"),
    path("principal/", c.principal_vista, name="principal"),
    path("salir/", c.salir_vista, name="salir"),
]