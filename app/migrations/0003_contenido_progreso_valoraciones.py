from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [("app", "0002_curso_inscripcioncurso"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.AddField(model_name="curso", name="objetivos", field=models.TextField(blank=True)),
        migrations.AddField(model_name="curso", name="requisitos", field=models.TextField(blank=True)),
        migrations.AddField(model_name="curso", name="instructor", field=models.CharField(blank=True, max_length=150)),
        migrations.AddField(model_name="curso", name="ofrece_certificado", field=models.BooleanField(default=True)),
        migrations.AddField(model_name="curso", name="publicado", field=models.BooleanField(default=True)),
        migrations.AlterField(model_name="curso", name="duracion_horas", field=models.PositiveIntegerField()),
        migrations.AlterField(model_name="curso", name="url_imagen", field=models.URLField(blank=True, max_length=500)),
        migrations.AddField(model_name="usuario", name="puede_gestionar_cursos", field=models.BooleanField(default=False)),
        migrations.CreateModel(name="Modulo", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("titulo", models.CharField(max_length=180)), ("descripcion", models.TextField(blank=True)), ("orden", models.PositiveIntegerField(default=1)), ("curso", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="modulos", to="app.curso"))], options={"db_table": "modulos_curso", "ordering": ["orden", "id"]}),
        migrations.CreateModel(name="Leccion", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("titulo", models.CharField(max_length=180)), ("contenido", models.TextField(blank=True)), ("url_video", models.URLField(blank=True, max_length=500)), ("duracion_minutos", models.PositiveIntegerField(default=0)), ("orden", models.PositiveIntegerField(default=1)), ("modulo", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lecciones", to="app.modulo"))], options={"db_table": "lecciones_curso", "ordering": ["orden", "id"]}),
        migrations.CreateModel(name="ProgresoLeccion", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("completado_en", models.DateTimeField(default=django.utils.timezone.now)), ("estudiante", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="progreso_lecciones", to=settings.AUTH_USER_MODEL)), ("leccion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="progresos", to="app.leccion"))], options={"db_table": "progreso_lecciones"}),
        migrations.AddConstraint(model_name="progresoleccion", constraint=models.UniqueConstraint(fields=("estudiante", "leccion"), name="progreso_unico_estudiante_leccion")),
        migrations.CreateModel(name="Valoracion", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("puntuacion", models.PositiveSmallIntegerField()), ("comentario", models.TextField(blank=True, max_length=1000)), ("creada_en", models.DateTimeField(auto_now_add=True)), ("curso", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="valoraciones", to="app.curso")), ("estudiante", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="valoraciones_curso", to=settings.AUTH_USER_MODEL))], options={"db_table": "valoraciones_curso", "ordering": ["-creada_en"]}),
        migrations.AddConstraint(model_name="valoracion", constraint=models.UniqueConstraint(fields=("estudiante", "curso"), name="valoracion_unica_estudiante_curso")),
    ]
