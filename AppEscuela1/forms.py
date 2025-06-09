from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Estudiante, Profesor, Curso, Entregable
import datetime

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Usuario o contraseña incorrectos")
        return cleaned_data
    
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Usuario",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

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