
from django.urls import path

from app.controlador import inicioController as inicio
from app.controlador import usuarioController as c
from app.controlador import recursosController as recursos
from app.controlador import instructoresController as instructores
from app.controlador import contactoController as contacto

urlpatterns = [
    path("", inicio.inicio_vista, name="inicio"),
    path("login/", c.login_vista, name="login"),
    path("registro/", c.registro_vista, name="registro"),
    path("principal/", c.principal_vista, name="principal"),
    path("perfil/", c.perfil_vista, name="perfil"),
    path("salir/", c.salir_vista, name="salir"),
    path("recursos/", recursos.seccion_recursos, name="recursos"),
    path("instructores/", instructores.seccion_instructores, name="instructores"),
    path("contacto/", contacto.seccion_contacto, name="contacto"),
    
] 
