import re

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from app.modelo.usuario import Usuario
from app.DAO.usuarioDao import UsuarioDAO, UsuarioDuplicado

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PLANTILLA = "loginUsuario.html"


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
        return redirect("principal")
 
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
 
        usuario = UsuarioDAO.buscar_por_email(email)
        if usuario is None or not usuario.check_password(password):
            contexto = {"errores": ["Correo o contraseña incorrectos."]}
            return render(request, PLANTILLA, contexto, status=401)
 
        login(request, usuario)
        if not request.POST.get("remember"):
            request.session.set_expiry(0)
        return redirect("principal")
 
    contexto = {
        "registrado": request.GET.get("registrado"),
        "mostrar_registro": request.GET.get("registro"),
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

    errores = _validar_registro(datos)
    if errores:
        contexto = {"errores": errores, "mostrar_registro": True}
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
                    "mostrar_registro": True}
        return render(request, PLANTILLA, contexto, status=409)

    return redirect("/?registrado=1")

def principal_vista(request):
    return render(request, "paginaPrincipal.html")

@login_required
def perfil_vista(request):
    return render(request, "perfilUsuario.html")

@require_POST
def salir_vista(request):
    logout(request)
    return redirect("login")