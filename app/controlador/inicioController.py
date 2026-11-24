from django.shortcuts import render

def inicio_vista(request):
    return render(request, "paginaPrincipal.html")