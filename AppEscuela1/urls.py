from django.urls import path
from .views import lista_estudiantes, detalle_estudiante, lista_profesores, index

app_name = 'AppEscuela1'

urlpatterns = [
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/<int:pk>/', detalle_estudiante, name='detalle_estudiante'),
    path('profesores/', lista_profesores, name='lista_profesores'),
    path("", index, name="index"),
]