from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from app.forms import CursoForm, LeccionForm, ModuloForm, ValoracionForm
from app.modelo.curso import Curso, Leccion, Modulo
from app.models import InscripcionCurso, ProgresoLeccion, Valoracion
from app.servicios.certificadoPdf import generar_certificado_pdf


def _anotar_progreso(curso, estudiante):
    total = Leccion.objects.filter(modulo__curso=curso).count()
    hechos = ProgresoLeccion.objects.filter(
        estudiante=estudiante, leccion__modulo__curso=curso
    ).count()
    curso.total_lecciones = total
    curso.lecciones_completadas = hechos
    curso.progreso = round(hechos * 100 / total) if total else 0
    curso.completado = bool(total and hechos >= total)
    curso.estado_estudio = "Completado" if curso.completado else "En curso"


def _destino(request, por_defecto):
    """Vuelve a la página indicada en 'next' (si es de este sitio) o a la ruta por defecto."""
    siguiente = request.POST.get("next", "")
    if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
        return siguiente
    return reverse(por_defecto)


def seccion_cursos(request, plantilla="cursos.html"):
    cursos = Curso.objects.filter(publicado=True).annotate(promedio=Avg("valoraciones__puntuacion"))
    busqueda = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    nivel = request.GET.get("nivel", "").strip()
    duracion = request.GET.get("duracion", "").strip()
    if busqueda:
        cursos = cursos.filter(Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda) | Q(instructor__icontains=busqueda))
    if categoria:
        cursos = cursos.filter(categoria__iexact=categoria)
    if nivel:
        cursos = cursos.filter(nivel__iexact=nivel)
    if duracion == "corto":
        cursos = cursos.filter(duracion_horas__lte=8)
    elif duracion == "medio":
        cursos = cursos.filter(duracion_horas__gt=8, duracion_horas__lte=20)
    elif duracion == "largo":
        cursos = cursos.filter(duracion_horas__gt=20)

    inscritos = set()
    if request.user.is_authenticated:
        inscritos = set(InscripcionCurso.objects.filter(estudiante=request.user).values_list("curso_id", flat=True))
        for curso in cursos:
            if curso.id_curso in inscritos:
                _anotar_progreso(curso, request.user)

    return render(request, plantilla, {
        "cursos": cursos, "categorias": Curso.objects.filter(publicado=True).values_list("categoria", flat=True).distinct().order_by("categoria"),
        "niveles": Curso.objects.filter(publicado=True).values_list("nivel", flat=True).distinct().order_by("nivel"),
        "categoria_actual": categoria, "nivel_actual": nivel, "duracion_actual": duracion,
        "busqueda": busqueda, "inscritos": inscritos,
    })


@login_required
def mis_cursos(request, plantilla="cursos.html"):
    cursos = [i.curso for i in InscripcionCurso.objects.filter(estudiante=request.user).select_related("curso").order_by("curso__nombre")]
    for curso in cursos:
        _anotar_progreso(curso, request.user)
    return render(request, plantilla, {"cursos": cursos, "inscritos": {c.id_curso for c in cursos}, "mis_cursos": True})


def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso.objects.annotate(promedio=Avg("valoraciones__puntuacion")), pk=curso_id)
    inscrito = request.user.is_authenticated and InscripcionCurso.objects.filter(estudiante=request.user, curso=curso).exists()
    if not curso.publicado and not inscrito:
        raise Http404("No se encontró el curso")
    completadas = set()
    if inscrito:
        completadas = set(ProgresoLeccion.objects.filter(estudiante=request.user, leccion__modulo__curso=curso).values_list("leccion_id", flat=True))
        _anotar_progreso(curso, request.user)
    curso.modulos_lista = curso.modulos.prefetch_related("lecciones").all()
    curso.valoraciones_lista = curso.valoraciones.select_related("estudiante")[:10]
    valoracion_existente = Valoracion.objects.filter(estudiante=request.user, curso=curso).first() if request.user.is_authenticated else None
    form_valoracion = ValoracionForm(instance=valoracion_existente)
    return render(request, "detalle_curso.html", {"curso": curso, "inscrito": inscrito, "completadas": completadas, "form_valoracion": form_valoracion})


def _curso_certificable(request, curso_id):
    """Devuelve el curso si el estudiante lo terminó; si no, avisa y devuelve None."""
    curso = get_object_or_404(Curso, pk=curso_id, ofrece_certificado=True)
    inscrito = InscripcionCurso.objects.filter(estudiante=request.user, curso=curso).exists()
    if not curso.publicado and not inscrito:
        raise Http404("No se encontró el curso")
    total = Leccion.objects.filter(modulo__curso=curso).count()
    completadas = ProgresoLeccion.objects.filter(estudiante=request.user, leccion__modulo__curso=curso).count()
    if not inscrito or total == 0 or completadas < total:
        messages.error(request, "Completa todas las lecciones para obtener tu certificado.")
        return None
    return curso


@login_required
def certificado_curso(request, curso_id):
    curso = _curso_certificable(request, curso_id)
    if curso is None:
        return redirect("detalle_curso", curso_id=curso_id)
    return render(request, "certificado.html", {"curso": curso, "estudiante": request.user, "emitido_en": timezone.localdate()})


@login_required
def descargar_certificado(request, curso_id):
    curso = _curso_certificable(request, curso_id)
    if curso is None:
        return redirect("detalle_curso", curso_id=curso_id)
    pdf = generar_certificado_pdf(request.user, curso, timezone.localdate())
    respuesta = HttpResponse(pdf, content_type="application/pdf")
    respuesta["Content-Disposition"] = f'attachment; filename="certificado-{slugify(curso.nombre)}.pdf"'
    return respuesta


@login_required
@require_POST
def inscribirse(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id, publicado=True)
    InscripcionCurso.objects.get_or_create(estudiante=request.user, curso=curso)
    messages.success(request, f"Te inscribiste en {curso.nombre}.")
    return redirect("detalle_curso", curso_id=curso.pk)


@login_required
@require_POST
def cancelar_inscripcion(request, curso_id):
    InscripcionCurso.objects.filter(estudiante=request.user, curso_id=curso_id).delete()
    messages.success(request, "Se quitó el curso de tu lista.")
    return redirect(_destino(request, "mis_cursos"))


@login_required
@require_POST
def completar_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion.objects.select_related("modulo__curso"), pk=leccion_id)
    curso = leccion.modulo.curso
    if not InscripcionCurso.objects.filter(estudiante=request.user, curso=curso).exists():
        messages.error(request, "Inscríbete en el curso para registrar tu avance.")
        return redirect("detalle_curso", curso_id=curso.pk)
    ProgresoLeccion.objects.get_or_create(estudiante=request.user, leccion=leccion)
    messages.success(request, "Lección marcada como completada.")
    return redirect(f"{reverse('detalle_curso', args=[curso.pk])}#leccion-{leccion.pk}")


@login_required
@require_POST
def valorar_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if not InscripcionCurso.objects.filter(estudiante=request.user, curso=curso).exists():
        messages.error(request, "Debes inscribirte antes de valorar este curso.")
        return redirect("detalle_curso", curso_id=curso.pk)
    valoracion = Valoracion.objects.filter(estudiante=request.user, curso=curso).first()
    form = ValoracionForm(request.POST, instance=valoracion)
    if form.is_valid():
        item = form.save(commit=False)
        item.estudiante, item.curso = request.user, curso
        item.save()
        messages.success(request, "Tu valoración quedó guardada.")
    else:
        messages.error(request, "Revisa la puntuación y vuelve a intentarlo.")
    return redirect("detalle_curso", curso_id=curso.pk)


def _gestor_requerido(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.puede_gestionar_cursos:
        messages.error(request, "Tu cuenta no tiene permiso para gestionar cursos.")
        return redirect("cursos")
    return None


@login_required
def gestionar_cursos(request):
    denegado = _gestor_requerido(request)
    if denegado:
        return denegado
    cursos = Curso.objects.prefetch_related("modulos__lecciones").all()
    for curso in cursos:
        curso.form_edicion = CursoForm(instance=curso)
    return render(request, "gestionar_cursos.html", {"cursos": cursos, "curso_form": CursoForm(), "modulo_form": ModuloForm(), "leccion_form": LeccionForm()})


@login_required
@require_POST
def guardar_curso(request, curso_id=None):
    denegado = _gestor_requerido(request)
    if denegado:
        return denegado
    curso = get_object_or_404(Curso, pk=curso_id) if curso_id else None
    form = CursoForm(request.POST, instance=curso)
    if form.is_valid():
        form.save()
        messages.success(request, "Curso guardado.")
        return redirect("gestionar_cursos")
    detalles_error = " ".join(f"{campo}: {', '.join(errores)}" for campo, errores in form.errors.items())
    messages.error(request, f"No se pudo guardar el curso. {detalles_error}")
    cursos = Curso.objects.prefetch_related("modulos__lecciones").all()
    for item in cursos:
        item.form_edicion = form if curso and item.pk == curso.pk else CursoForm(instance=item)
    formulario_creacion = CursoForm() if curso else form
    return render(request, "gestionar_cursos.html", {"cursos": cursos, "curso_form": formulario_creacion, "modulo_form": ModuloForm(), "leccion_form": LeccionForm()})


@login_required
@require_POST
def guardar_modulo(request, curso_id):
    denegado = _gestor_requerido(request)
    if denegado:
        return denegado
    curso = get_object_or_404(Curso, pk=curso_id)
    form = ModuloForm(request.POST)
    if form.is_valid():
        modulo = form.save(commit=False)
        modulo.curso = curso
        modulo.save()
        messages.success(request, "Módulo agregado.")
    else:
        detalles_error = " ".join(f"{campo}: {', '.join(errores)}" for campo, errores in form.errors.items())
        messages.error(request, f"No se pudo agregar el módulo. {detalles_error}")
    return redirect("gestionar_cursos")


@login_required
@require_POST
def guardar_leccion(request, modulo_id):
    denegado = _gestor_requerido(request)
    if denegado:
        return denegado
    modulo = get_object_or_404(Modulo, pk=modulo_id)
    form = LeccionForm(request.POST)
    if form.is_valid():
        leccion = form.save(commit=False)
        leccion.modulo = modulo
        leccion.save()
        messages.success(request, "Lección agregada.")
    else:
        detalles_error = " ".join(f"{campo}: {', '.join(errores)}" for campo, errores in form.errors.items())
        messages.error(request, f"No se pudo agregar la lección. {detalles_error}")
    return redirect("gestionar_cursos")
