from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = 'AppEscuela1'

urlpatterns = [
    path("", index, name="index"),
    path('login/', login_usuario, name='login_usuario'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('logout/', logout_usuario, name='logout_usuario'),     
    path('perfil', perfil, name='perfil'),
    path('editar_perfil', editar_perfil, name='editar_perfil'),
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/nuevo/', crear_estudiante, name='crear_estudiante'),     
    path('estudiantes/<int:pk>/', detalle_estudiante, name='detalle_estudiante'),
    path("estudiantes/<int:pk>/editar/", editar_estudiante, name="editar_estudiante"),
    path('estudiantes/eliminar/<int:pk>/', eliminar_estudiante, name='eliminar_estudiante'),   
    path('profesores/', lista_profesores, name='lista_profesores'),
    path('profesores/nuevo/', crear_profesor, name='crear_profesor'),    
    path('profesores/<int:pk>/', detalle_profesores, name='detalle_profesores'),
    path("profesores/<int:pk>/editar/", editar_profesor, name="editar_profesor"),
    path('profesores/eliminar/<int:pk>/', eliminar_profesor, name='eliminar_profesor'),      
    path('cursos/', lista_cursos, name='lista_cursos'),
    path('cursos/nuevo/', crear_curso, name='crear_curso'),    
    path('cursos/<int:pk>', detalle_cursos, name='detalle_cursos'),
    path("cursos/<int:pk>/editar/", editar_curso, name="editar_curso"),
    path('cursos/eliminar/<int:pk>/', eliminar_curso, name='eliminar_curso'),    
    path('entregables/', lista_entregable, name='lista_entregables'),
    path('entregables/nuevo/', crear_entregable, name='crear_entregable'),    
    path('entregables/<int:pk>/', detalle_entregable, name='detalle_entregable'),
    path("entregables/<int:pk>/editar/", editar_entregable, name="editar_entregable"),
    path('entregables/eliminar/<int:pk>/', eliminar_entregable, name='eliminar_entregable'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)