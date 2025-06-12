from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Estudiante, Profesor, Curso, Entregable, Avatar
from .forms import EstudianteForm, ProfesorForm, CursoForm, EntregableForm, LoginForm, RegistroForm, EditUserForm , AvatarForm

def index(request):
    return render(request, 'AppEscuela1/index.html')

def about(request):
    return render(request, 'AppEscuela1/about.html')

# Creación/Login Usuarios

def login_usuario(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.user)
        return redirect('AppEscuela1:index')
    return render(request, 'AppEscuela1/login.html', {'form': form})

@require_POST
def logout_usuario(request):
    if request.method == 'POST':
        logout(request)
    return redirect('AppEscuela1:index')

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Crear avatar
            profesion = form.cleaned_data.get('profesion')
            uploaded_imagen = form.cleaned_data.get('avatar')
            Avatar.objects.create(user=user, profesion=profesion, imagen=uploaded_imagen)

            login(request, user)
            return redirect('AppEscuela1:index')
    else:
        form = RegistroForm()
    return render(request, "AppEscuela1/registrar.html", {"form": form})

@login_required
def perfil(request):
    return render(request, "AppEscuela1/perfil.html", {"usuario": request.user, "avatar":getattr(request.user, 'avatar', None)})

# Listas y Detalles

class lista_estudiantes(ListView):
    model = Estudiante
    template_name = 'AppEscuela1/estudiantes_list.html'
    context_object_name = 'estudiantes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Estudiante.objects.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query)
            )
        return Estudiante.objects.all()

@login_required(login_url='AppEscuela1:login_usuario')
def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'AppEscuela1/estudiante_detail.html', {'estudiante': estudiante})

class lista_profesores(ListView):
    model = Profesor
    template_name = 'AppEscuela1/profesores_list.html'
    context_object_name = 'profesores'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Profesor.objects.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query)
            )
        return Profesor.objects.all()

@login_required(login_url='AppEscuela1:login_usuario')
def detalle_profesores(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    return render(request, 'AppEscuela1/profesores_detail.html', {'profesor': profesor})

class lista_cursos(ListView):
    model = Curso
    template_name = 'AppEscuela1/cursos_list.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Curso.objects.filter(
                Q(nombre__icontains=query)
            )
        return Curso.objects.all()

@login_required(login_url='AppEscuela1:login_usuario')
def detalle_cursos(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'AppEscuela1/cursos_detail.html', {'curso': curso})

class lista_entregable(ListView):
    model = Entregable
    template_name = 'AppEscuela1/entregable_list.html'
    context_object_name = 'entregables'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Entregable.objects.filter(
                Q(nombre__icontains=query) |
                Q(curso__nombre__icontains=query)
            )
        return Entregable.objects.all()

@login_required(login_url='AppEscuela1:login_usuario')
def detalle_entregable(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)
    return render(request, 'AppEscuela1/entregable_detail.html', {'entregable': entregable})

# Creación de Elementos

class crear_estudiante(LoginRequiredMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'AppEscuela1/estudiante_form.html'
    success_url = '/estudiantes/'

    login_url = 'AppEscuela1:login_usuario'

class crear_profesor(LoginRequiredMixin, CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'AppEscuela1/profesor_form.html'
    success_url = '/profesores/'

    login_url = 'AppEscuela1:login_usuario'

class crear_curso(LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'AppEscuela1/curso_form.html'
    success_url = '/cursos/'

    login_url = 'AppEscuela1:login_usuario'

class crear_entregable(LoginRequiredMixin, CreateView):
    model = Entregable
    form_class = EntregableForm
    template_name = 'AppEscuela1/entregable_form.html'
    success_url = '/entregables/'

    login_url = 'AppEscuela1:login_usuario'

# Editar Elementos

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

@login_required
def editar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == "POST":
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect("AppEscuela1:detalle_estudiante", pk=estudiante.pk)
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, "AppEscuela1/estudiante_form.html", {"form": form})

@login_required
def editar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == "POST":
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect("AppEscuela1:detalle_profesores", pk=profesor.pk)
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, "AppEscuela1/profesor_form.html", {"form": form})

@login_required
def editar_curso(request, pk):
    cursos = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        form = CursoForm(request.POST, instance=cursos)
        if form.is_valid():
            form.save()
            return redirect("AppEscuela1:detalle_cursos", pk=cursos.pk)
    else:
        form = CursoForm(instance=cursos)
    return render(request, "AppEscuela1/curso_form.html", {"form": form})

@login_required
def editar_entregable(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)
    if request.method == "POST":
        form = EntregableForm(request.POST, instance=entregable)
        if form.is_valid():
            form.save()
            return redirect("AppEscuela1:detalle_entregable", pk=entregable.pk)
    else:
        form = EntregableForm(instance=entregable)
    return render(request, "AppEscuela1/entregable_form.html", {"form": form})

# Eliminar Elementos

@login_required
def eliminar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == "POST":
        estudiante.delete()
        return redirect('AppEscuela1:lista_estudiantes') 
    return render(request, "AppEscuela1/confirmar_eliminar.html", {"objeto": estudiante})

@login_required
def eliminar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == "POST":
        profesor.delete()
        return redirect('AppEscuela1:lista_profesores')
    return render(request, "AppEscuela1/confirmar_eliminar.html", {"objeto": profesor})

@login_required
def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        curso.delete()
        return redirect('AppEscuela1:lista_cursos') 
    return render(request, "AppEscuela1/confirmar_eliminar.html", {"objeto": curso})

@login_required
def eliminar_entregable(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)
    if request.method == "POST":
        entregable.delete()
        return redirect('AppEscuela1:lista_entregables')
    return render(request, "AppEscuela1/confirmar_eliminar.html", {"objeto": entregable})
