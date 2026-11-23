from app.modelo.curso import Leccion
from app.models import InscripcionCurso, ProgresoLeccion


class CursoDAO:
    @staticmethod
    def cursos_del_estudiante(usuario):
        """Cursos en los que está inscrito, del más reciente al más antiguo,
        con el avance calculado (progreso, completado, lecciones)."""
        inscripciones = (
            InscripcionCurso.objects.filter(estudiante=usuario)
            .select_related("curso")
            .order_by("-inscrito_en")
        )
        cursos = []
        for inscripcion in inscripciones:
            curso = inscripcion.curso
            total = Leccion.objects.filter(modulo__curso=curso).count()
            hechas = ProgresoLeccion.objects.filter(
                estudiante=usuario, leccion__modulo__curso=curso
            ).count()
            curso.total_lecciones = total
            curso.lecciones_completadas = hechas
            curso.progreso = round(hechas * 100 / total) if total else 0
            curso.completado = bool(total and hechas >= total)
            cursos.append(curso)
        return cursos