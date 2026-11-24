from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.DAO.cursoDao import CursoDAO
from app.forms import CambiarContrasenaForm, PerfilUsuarioForm


@login_required
def panel_movil(request):
    cursos = CursoDAO.cursos_del_estudiante(request.user)
    completados = [c for c in cursos if c.completado]
    en_curso = [c for c in cursos if not c.completado]

    return render(request, "movil/panelMovil.html", {
        "total_cursos": len(cursos),
        "total_completados": len(completados),
        "competencias": completados,  # un curso completado valida su competencia
        "curso_actual": en_curso[0] if en_curso else None,
        # Pendiente: se llenarán desde la base de datos cuando existan talleres y ofertas
        "taller": None,
        "ofertas": [],
    })


@login_required
def perfil_movil(request):
    formulario = PerfilUsuarioForm(instance=request.user)
    formulario_contrasena = CambiarContrasenaForm(request.user)

    if request.method == "POST":
        if request.POST.get("accion") == "contrasena":
            formulario_contrasena = CambiarContrasenaForm(request.user, request.POST)
            if formulario_contrasena.is_valid():
                request.user.set_password(formulario_contrasena.cleaned_data["nueva_contrasena"])
                request.user.save(update_fields=["password"])
                update_session_auth_hash(request, request.user)  # mantiene la sesión abierta
                messages.success(request, "Tu contraseña se cambió correctamente.")
                return redirect("perfil_movil")
        else:
            formulario = PerfilUsuarioForm(request.POST, instance=request.user)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, "Tus datos se actualizaron correctamente.")
                return redirect("perfil_movil")
        messages.error(request, "Revisa los campos e inténtalo de nuevo.")

    cursos = CursoDAO.cursos_del_estudiante(request.user)
    return render(request, "movil/perfilMovil.html", {
        "formulario": formulario,
        "formulario_contrasena": formulario_contrasena,
        "total_cursos": len(cursos),
        "total_completados": sum(1 for c in cursos if c.completado),
        "total_lecciones": sum(c.lecciones_completadas for c in cursos),
    })