import re
from urllib.parse import urlencode

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from urllib.parse import urlencode

from app.modelo.usuario import Usuario
from app.modelo.curso import Curso
from app.DAO.usuarioDao import UsuarioDAO, UsuarioDuplicado
from app.forms import CambiarContrasenaForm, PerfilUsuarioForm
from app.models import InscripcionCurso, ProgresoLeccion, Valoracion

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PLANTILLA = "loginUsuario.html"


def _redireccion_segura(request, destino=None):
    destino = destino or request.POST.get("next") or request.GET.get("next")
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return redirect(destino)
    return redirect("inicio")


def _validar_registro(d: dict) -> list:
    """La validación del servidor es obligatoria: la del HTML se puede saltar."""
    errores = []
    if not d["nombres"] or not d["apellidos"]:
        errores.append("Nombres y apellidos son obligatorios.")
    if not re.fullmatch(r"\d{8}", d["dni"]):
        errores.append("El DNI debe tener 8 dígitos.")
    if not re.fullmatch(r"\d{9}", d["telefono"]):
        errores.append("El teléfono debe tener 9 dígitos.")
    if not EMAIL_RE.match(d["email"]):
        errores.append("El correo electrónico no es válido.")
    if len(d["password"]) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres.")
    if not d["terminos"]:
        errores.append("Debes aceptar los términos y condiciones.")
    return errores


def login_vista(request):
    if request.user.is_authenticated:
        return _redireccion_segura(request)
 
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
 
        usuario = UsuarioDAO.buscar_por_email(email)
        if usuario is None or not usuario.check_password(password):
            contexto = {"errores": ["Correo o contraseña incorrectos."], "next": request.POST.get("next", "")}
            return render(request, PLANTILLA, contexto, status=401)
 
        login(request, usuario)
        if not request.POST.get("remember"):
            request.session.set_expiry(0)
        return _redireccion_segura(request)
 
    contexto = {
        "registrado": request.GET.get("registrado"),
        "mostrar_registro": request.GET.get("registro"),
        "next": request.GET.get("next", ""),
    }
    return render(request, PLANTILLA, contexto)


def registro_vista(request):
    if request.method != "POST":
        return redirect("login")

    datos = {
        "nombres": request.POST.get("nombres", "").strip(),
        "apellidos": request.POST.get("apellidos", "").strip(),
        "dni": request.POST.get("dni", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
        "email": request.POST.get("email", "").strip().lower(),
        "password": request.POST.get("password", ""),
        "terminos": request.POST.get("terminos"),
    }
    datos_reingreso = {campo: datos[campo] for campo in ("nombres", "apellidos", "dni", "telefono", "email")}

    errores = _validar_registro(datos)
    if errores:
        contexto = {"errores": errores, "mostrar_registro": True, "datos_registro": datos_reingreso, "next": request.POST.get("next", "")}
        return render(request, PLANTILLA, contexto, status=400)

    usuario = Usuario(
        nombres=datos["nombres"],
        apellidos=datos["apellidos"],
        dni=datos["dni"],
        telefono=datos["telefono"],
        email=datos["email"],
    )
    usuario.set_password(datos["password"]) 

    try:
        UsuarioDAO.guardar(usuario)
    except UsuarioDuplicado:
        contexto = {"errores": ["Ya existe una cuenta con ese correo o DNI."],
                    "mostrar_registro": True, "datos_registro": datos_reingreso, "next": request.POST.get("next", "")}
        return render(request, PLANTILLA, contexto, status=409)

    destino = request.POST.get("next", "")
    query = {"registrado": "1"}
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        query["next"] = destino
    return redirect(f"{reverse('login')}?{urlencode(query)}")


def terminos_vista(request):
    return render(request, "terminos.html", {"next": request.GET.get("next", "")})

def principal_vista(request):
    return redirect("inicio")

@login_required
def perfil_vista(request):
    formulario = PerfilUsuarioForm(instance=request.user)
    formulario_contrasena = CambiarContrasenaForm(request.user)
    if request.method == "POST":
        if request.POST.get("accion") == "contrasena":
            formulario_contrasena = CambiarContrasenaForm(request.user, request.POST)
            if formulario_contrasena.is_valid():
                request.user.set_password(formulario_contrasena.cleaned_data["nueva_contrasena"])
                request.user.save(update_fields=["password"])
                update_session_auth_hash(request, request.user)
                messages.success(request, "Tu contraseña se cambió correctamente.")
                return redirect("perfil")
            messages.error(request, "No se pudo cambiar la contraseña. Revisa los campos.")
        else:
            formulario = PerfilUsuarioForm(request.POST, instance=request.user)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, "Tus datos se actualizaron correctamente.")
                return redirect("perfil")
            messages.error(request, "Revisa los campos e inténtalo de nuevo.")

    inscripciones = InscripcionCurso.objects.filter(estudiante=request.user).select_related("curso").order_by("-inscrito_en")
    cursos = []
    lecciones_completadas_total = 0
    categorias_usuario = set()
    for inscripcion in inscripciones:
        curso = inscripcion.curso
        total = curso.modulos.aggregate(total=Count("lecciones"))["total"] or 0
        completadas = ProgresoLeccion.objects.filter(estudiante=request.user, leccion__modulo__curso=curso).count()
        curso.total_lecciones = total
        curso.lecciones_completadas = completadas
        curso.progreso = round(completadas * 100 / total) if total else 0
        curso.completado = bool(total and completadas >= total)
        lecciones_completadas_total += completadas
        categorias_usuario.add(curso.categoria)
        cursos.append(curso)
    cursos_completados = sum(1 for curso in cursos if curso.completado)
    categorias = list(Curso.objects.filter(publicado=True).values_list("categoria", flat=True).distinct().order_by("categoria"))
    ids_inscritos = [inscripcion.curso_id for inscripcion in inscripciones]
    recomendaciones = Curso.objects.filter(publicado=True).exclude(pk__in=ids_inscritos)
    if categorias_usuario:
        personalizadas = Curso.objects.filter(
            publicado=True, categoria__in=categorias_usuario
        ).exclude(pk__in=ids_inscritos).order_by("nombre")
        if personalizadas.exists():
            recomendaciones = personalizadas
    recomendaciones = recomendaciones.order_by("nombre")[:4]
    valoraciones = Valoracion.objects.filter(estudiante=request.user).select_related("curso").order_by("-creada_en")[:5]
    actividad_reciente = ProgresoLeccion.objects.filter(
        estudiante=request.user
    ).select_related("leccion__modulo__curso").order_by("-completado_en")[:5]
    return render(request, "perfilUsuario.html", {
        "formulario": formulario, "formulario_contrasena": formulario_contrasena,
        "cursos": cursos, "total_cursos": len(cursos),
        "cursos_completados": cursos_completados,
        "lecciones_completadas_total": lecciones_completadas_total,
        "categorias": categorias, "recomendaciones": recomendaciones,
        "valoraciones": valoraciones, "actividad_reciente": actividad_reciente,
        "total_valoraciones": Valoracion.objects.filter(estudiante=request.user).count(),
        "promedio_valoraciones": Valoracion.objects.filter(estudiante=request.user).aggregate(promedio=Avg("puntuacion"))["promedio"],
    })

@require_POST
def salir_vista(request):
    logout(request)
    return redirect("login")
