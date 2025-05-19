from django import forms
from .models import Estudiante, Profesor, Curso, Entregable
import datetime

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if Estudiante.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un estudiante con este correo.")
        return email

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido', 'email', 'profesion']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Profesor.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un profesor con este correo.")
        return email
    
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'camada', 'profesor']
    
    def clean_camada(self):
        camada = self.cleaned_data['camada']
        if camada <= 0:
            raise forms.ValidationError("La camada debe ser un número positivo.")
        return camada

class EntregableForm(forms.ModelForm):
    class Meta:
        model = Entregable
        fields = ['nombre', 'descripcion', 'curso', 'fecha_entrega']
        widgets = {
            'fecha_entrega': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        }
    
    def clean_fecha_entrega(self):
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise forms.ValidationError("La fecha de entrega no puede ser en el pasado.")
        return fecha