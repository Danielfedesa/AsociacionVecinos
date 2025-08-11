from django.shortcuts import render

def home(request):
    return render(request, "core/home.html")

def actividades(request):
    return render(request, "core/actividades.html")

def horarios(request):
    return render(request, "core/horarios.html")

def contacto(request):
    return render(request, "core/contacto.html")