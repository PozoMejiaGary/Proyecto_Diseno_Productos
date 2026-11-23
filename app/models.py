from django.db import models
from django.utils import timezone

from app.modelo.curso import Curso, Leccion, Modulo
from app.modelo.usuario import Usuario


class InscripcionCurso(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="inscripciones_curso")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="inscripciones")
    inscrito_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inscripciones_curso"
        constraints = [models.UniqueConstraint(fields=["estudiante", "curso"], name="inscripcion_unica_estudiante_curso")]
        ordering = ["-inscrito_en"]

    def __str__(self):
        return f"{self.estudiante} — {self.curso}"


class ProgresoLeccion(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="progreso_lecciones")
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="progresos")
    completado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "progreso_lecciones"
        constraints = [models.UniqueConstraint(fields=["estudiante", "leccion"], name="progreso_unico_estudiante_leccion")]


class Valoracion(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="valoraciones_curso")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="valoraciones")
    puntuacion = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True, max_length=1000)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "valoraciones_curso"
        constraints = [models.UniqueConstraint(fields=["estudiante", "curso"], name="valoracion_unica_estudiante_curso")]
        ordering = ["-creada_en"]

    def __str__(self):
        return f"{self.curso}: {self.puntuacion}/5"
