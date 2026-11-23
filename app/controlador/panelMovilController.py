from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.DAO.cursoDao import CursoDAO


@login_required
def panel_movil(request):
    cursos = CursoDAO.cursos_del_estudiante(request.user)
    completados = [c for c in cursos if c.completado]
    en_curso = [c for c in cursos if not c.completado]

    return render(request, "movil/panelMovil.html", {
        "total_cursos": len(cursos),
        "total_completados": len(completados),
        "competencias": completados,
        "curso_actual": en_curso[0] if en_curso else None,
        "taller": None,
        "ofertas": [],
    })