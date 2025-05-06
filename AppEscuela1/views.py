from django.shortcuts import render, get_object_or_404
from .models import Estudiante, Profesor, Curso, Entregable

def index(request):
    return render(request, 'AppEscuela1/index.html')

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    contexto = {
        'estudiantes': estudiantes
    }
    return render(request, 'AppEscuela1/estudiantes_list.html', contexto)

def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'AppEscuela1/estudiante_detail.html', {'estudiante': estudiante})

def lista_profesores(request):
    profesores = Profesor.objects.all()
    contexto = {
        'profesores': profesores
    }
    return render(request, 'AppEscuela1/profesores_list.html', contexto)