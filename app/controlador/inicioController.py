from django.shortcuts import render

CURSOS_EJEMPLO = [
    {"titulo": "Excel Básico a Avanzado", "categoria": "Tecnología", "nivel": "Principiante",
     "horas": 12, "alumnos": "1,240", "icono": "💻", "tema": "azul"},
    {"titulo": "Comunicación Efectiva", "categoria": "Comunicación", "nivel": "Principiante",
     "horas": 8, "alumnos": "980", "icono": "🗣️", "tema": "verde"},
    {"titulo": "Entrevista Laboral Exitosa", "categoria": "Empleabilidad", "nivel": "Intermedio",
     "horas": 6, "alumnos": "2,100", "icono": "💼", "tema": "coral"},
    {"titulo": "CV Profesional desde Cero", "categoria": "Empleabilidad", "nivel": "Principiante",
     "horas": 4, "alumnos": "3,300", "icono": "📄", "tema": "amarillo"},
    {"titulo": "Finanzas Personales", "categoria": "Finanzas", "nivel": "Principiante",
     "horas": 10, "alumnos": "860", "icono": "📊", "tema": "azul"},
    {"titulo": "Liderazgo y Trabajo en Equipo", "categoria": "Liderazgo", "nivel": "Intermedio",
     "horas": 14, "alumnos": "720", "icono": "🚀", "tema": "verde"},
]

def inicio_vista(request):
    return render(request, "paginaPrincipal.html", {"cursos": CURSOS_EJEMPLO})