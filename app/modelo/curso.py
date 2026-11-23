from django.db import models


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    duracion_horas = models.PositiveIntegerField()
    url_imagen = models.URLField(max_length=500, blank=True)
    objetivos = models.TextField(blank=True)
    requisitos = models.TextField(blank=True)
    instructor = models.CharField(max_length=150, blank=True)
    ofrece_certificado = models.BooleanField(default=True)
    publicado = models.BooleanField(default=True)

    class Meta:
        db_table = "cursos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="modulos")
    titulo = models.CharField(max_length=180)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "modulos_curso"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.curso.nombre}: {self.titulo}"


class Leccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="lecciones")
    titulo = models.CharField(max_length=180)
    contenido = models.TextField(blank=True)
    url_video = models.URLField(max_length=500, blank=True)
    duracion_minutos = models.PositiveIntegerField(default=0)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "lecciones_curso"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo
