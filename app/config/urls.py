from django.urls import path

from app.controlador import inicioController as inicio
from app.controlador import usuarioController as c
from app.controlador import recursosController as recursos
from app.controlador import cursosController as cursos

urlpatterns = [
    path("", inicio.inicio_vista, name="inicio"),
    path("login/", c.login_vista, name="login"),
    path("registro/", c.registro_vista, name="registro"),
    path("principal/", c.principal_vista, name="principal"),
    path("perfil/", c.perfil_vista, name="perfil"),
    path("salir/", c.salir_vista, name="salir"),
    path("recursos/", recursos.seccion_recursos, name="recursos"),
    path("cursos/", cursos.seccion_cursos, name="cursos"),
    path("mis-cursos/", cursos.mis_cursos, name="mis_cursos"),
    path("cursos/<int:curso_id>/", cursos.detalle_curso, name="detalle_curso"),
    path("cursos/<int:curso_id>/inscribirse/", cursos.inscribirse, name="inscribirse"),
    path("cursos/<int:curso_id>/cancelar/", cursos.cancelar_inscripcion, name="cancelar_inscripcion"),
    path("lecciones/<int:leccion_id>/completar/", cursos.completar_leccion, name="completar_leccion"),
    path("cursos/<int:curso_id>/valorar/", cursos.valorar_curso, name="valorar_curso"),
    path("gestionar-cursos/", cursos.gestionar_cursos, name="gestionar_cursos"),
    path("gestionar-cursos/guardar/", cursos.guardar_curso, name="crear_curso"),
    path("gestionar-cursos/<int:curso_id>/guardar/", cursos.guardar_curso, name="editar_curso"),
    path("gestionar-cursos/<int:curso_id>/modulos/", cursos.guardar_modulo, name="crear_modulo"),
    path("gestionar-modulos/<int:modulo_id>/lecciones/", cursos.guardar_leccion, name="crear_leccion"),
]
