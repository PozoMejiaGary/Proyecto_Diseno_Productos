# Generated for the course catalog and student selections.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Curso",
            fields=[
                ("id_curso", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=150)),
                ("descripcion", models.TextField()),
                ("categoria", models.CharField(max_length=100)),
                ("nivel", models.CharField(max_length=50)),
                ("duracion_horas", models.IntegerField()),
                ("url_imagen", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={"db_table": "cursos"},
        ),
        migrations.CreateModel(
            name="InscripcionCurso",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("inscrito_en", models.DateTimeField(auto_now_add=True)),
                ("curso", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inscripciones", to="app.curso")),
                ("estudiante", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inscripciones_curso", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "inscripciones_curso", "ordering": ["-inscrito_en"]},
        ),
        migrations.AddConstraint(
            model_name="inscripcioncurso",
            constraint=models.UniqueConstraint(fields=("estudiante", "curso"), name="inscripcion_unica_estudiante_curso"),
        ),
    ]
