from django.urls import path

from app.controlador import inicioController as inicio
from app.controlador import usuarioController as c
<<<<<<< HEAD
from app.controlador import recursosController as recursos
=======
>>>>>>> 3da1fcba777c30e6723dc6f98b8ca89e8cc7ea5a

urlpatterns = [
    path("", inicio.inicio_vista, name="inicio"),
    path("login/", c.login_vista, name="login"),
    path("registro/", c.registro_vista, name="registro"),
    path("principal/", c.principal_vista, name="principal"),
    path("perfil/", c.perfil_vista, name="perfil"),
    path("salir/", c.salir_vista, name="salir"),
<<<<<<< HEAD
    path("recursos/", recursos.seccion_recursos, name="recursos"),
] 
=======
]
>>>>>>> 3da1fcba777c30e6723dc6f98b8ca89e8cc7ea5a
