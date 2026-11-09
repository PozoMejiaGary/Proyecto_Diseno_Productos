from django.shortcuts import render

def seccion_contacto(request):
    return render(request, 'contacto.html')