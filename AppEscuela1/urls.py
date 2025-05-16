from django.urls import path
from .views import *

app_name = 'AppEscuela1'

urlpatterns = [
    path("", index, name="index"),
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/<int:pk>/', detalle_estudiante, name='detalle_estudiante'),
    path('profesores/', lista_profesores, name='lista_profesores'),
    path('profesores/<int:pk>/', detalle_profesores, name='detalle_profesores'),
    path('cursos/', lista_cursos, name='lista_cursos'),
    path('cursos/<int:pk>', detalle_cursos, name='detalle_cursos'),
    path('entregables/', lista_entregable, name='lista_entregables'),
    path('entregables/<int:pk>/', detalle_entregable, name='detalle_entregable'),
    path('estudiantes/nuevo/', crear_estudiante, name='crear_estudiante'),
    path('profesores/nuevo/', crear_profesor, name='crear_profesor'),
    path('cursos/nuevo/', crear_curso, name='crear_curso'),
    path('entregables/nuevo/', crear_entregable, name='crear_entregable'),
    
]