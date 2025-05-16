from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Estudiante, Profesor, Curso, Entregable
from .forms import EstudianteForm, ProfesorForm, CursoForm, EntregableForm

def index(request):
    return render(request, 'AppEscuela1/index.html')

def lista_estudiantes(request):
    query = request.GET.get('q')
    if query:
        estudiantes = Estudiante.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        )
    else:
        estudiantes = Estudiante.objects.all()

    contexto = {
        'estudiantes': estudiantes,
        'query': query,
    }
    return render(request, 'AppEscuela1/estudiantes_list.html', contexto)


def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'AppEscuela1/estudiante_detail.html', {'estudiante': estudiante})

def lista_profesores(request):
    query = request.GET.get('q')
    if query:
        profesores = Profesor.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        )
    else:
        profesores = Profesor.objects.all()

    contexto = {
        'profesores': profesores,
        'query': query,
    }
    return render(request, 'AppEscuela1/profesores_list.html', contexto)

def detalle_profesores(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    return render(request, 'AppEscuela1/profesores_detail.html', {'profesor': profesor})

def lista_cursos(request):
    query = request.GET.get('q')
    if query:
        cursos = Curso.objects.filter(
            Q(nombre__icontains=query)
        )
    else:
        cursos = Curso.objects.all()

    contexto = {
        'cursos': cursos,
        'query': query,
    }
    return render(request, 'AppEscuela1/cursos_list.html', contexto)

def detalle_cursos(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'AppEscuela1/cursos_detail.html', {'curso': curso})

def lista_entregable(request):
    query = request.GET.get('q')
    if query:
        entregable = Entregable.objects.filter(
            Q(nombre__icontains=query) |
            Q(curso__icontains=query)
        )
    else:
        entregable = Entregable.objects.all()

    contexto = {
        'entregable': entregable,
        'query': query,
    }
    return render(request, 'AppEscuela1/entregable_list.html', contexto)

def detalle_entregable(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)
    return render(request, 'AppEscuela1/entregable_detail.html', {'entregable': entregable})

def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppEscuela1:lista_estudiantes')
    else:
        form = EstudianteForm()
    return render(request, 'AppEscuela1/estudiante_form.html', {'form': form})

def crear_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppEscuela1:lista_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'AppEscuela1/profesor_form.html', {'form': form})

def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppEscuela1:lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'AppEscuela1/curso_form.html', {'form': form})

def crear_entregable(request):
    if request.method == 'POST':
        form = EntregableForm(request.POST)
        if form.is_valid():
            print("Formulario Valido")
            form.save()
            return redirect('AppEscuela1:lista_entregables')
        else:
            print(form.errors)
    else:
        form = EntregableForm()
    return render(request, 'AppEscuela1/entregable_form.html', {'form': form})