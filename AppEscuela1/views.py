from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Estudiante, Profesor, Curso, Entregable, Avatar
from .forms import EstudianteForm, ProfesorForm, CursoForm, EntregableForm, LoginForm, RegistroForm, EditUserForm , AvatarForm

def index(request):
    return render(request, 'AppEscuela1/index.html')

def login_usuario(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            return redirect('AppEscuela1:index')
        else:
            form.add_error(None, "Usuario o contraseña incorrectos")
    return render(request, 'AppEscuela1/login.html', {'form': form})

@require_POST
def logout_usuario(request):
    if request.method == 'POST':
        logout(request)
    return redirect('AppEscuela1:index')

def registro_usuario(request):
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'AppEscuela1/registrar.html', {'form': form})

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


@login_required(login_url='AppEscuela1:login_usuario')
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

@login_required(login_url='AppEscuela1:login_usuario')
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

@login_required(login_url='AppEscuela1:login_usuario')
def detalle_cursos(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'AppEscuela1/cursos_detail.html', {'curso': curso})

def lista_entregable(request):
    query = request.GET.get('q')
    if query:
        entregables = Entregable.objects.filter(
            Q(nombre__icontains=query) |
            Q(curso__nombre__icontains=query)
        )
    else:
        entregables = Entregable.objects.all()

    contexto = {
        'entregables': entregables,
        'query': query,
    }
    return render(request, 'AppEscuela1/entregable_list.html', contexto)

@login_required(login_url='AppEscuela1:login_usuario')
def detalle_entregable(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)
    return render(request, 'AppEscuela1/entregable_detail.html', {'entregable': entregable})

@login_required(login_url='AppEscuela1:login_usuario')
def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppEscuela1:lista_estudiantes')
    else:
        form = EstudianteForm()
    return render(request, 'AppEscuela1/estudiante_form.html', {'form': form})

@login_required(login_url='AppEscuela1:login_usuario')
def crear_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppEscuela1:lista_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'AppEscuela1/profesor_form.html', {'form': form})

@login_required(login_url='AppEscuela1:login_usuario')
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppEscuela1:lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'AppEscuela1/curso_form.html', {'form': form})

@login_required(login_url='AppEscuela1:login_usuario')
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

@login_required
def perfil(request):
    return render(request, "AppEscuela1/perfil.html", {"usuario": request.user, "avatar":getattr(request.user, 'avatar', None)})

@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user)
        
        try:
            avatar = request.user.avatar
        except Avatar.DoesNotExist:
            avatar = None
        
        if avatar:
            avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        else:
            avatar_form = AvatarForm(request.POST, request.FILES)
        
        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar_instance = avatar_form.save(commit=False)
            avatar_instance.user = request.user
            avatar_instance.save()
            return redirect('AppEscuela1:perfil')
    else:
        form = EditUserForm(instance=request.user)
        if hasattr(request.user, "avatar"):
            avatar_form = AvatarForm(instance=request.user.avatar)
        else:
            avatar_form = AvatarForm()
    return render(request, 'AppEscuela1/editar_perfil.html', {"form": form, "avatar_form": avatar_form})