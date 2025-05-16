from django import forms
from .models import Estudiante, Profesor, Curso, Entregable

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'email']

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido', 'email', 'profesion']
    
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'camada', 'profesor']

class EntregableForm(forms.ModelForm):
    class Meta:
        model = Entregable
        fields = ['nombre', 'descripcion', 'curso', 'fecha_entrega']
        widgets = {
            'fecha_entrega': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        }
    