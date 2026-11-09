from django.shortcuts import render

def seccion_instructores(request):
    return render(request, 'instructores.html')