from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Estudiante, Profesor, Curso, Entregable, Avatar
import datetime

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email", "").lower().strip()
        password = cleaned_data.get("password")

        if email and password:
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(username=user_obj.username, password=password)
                if user is None:
                    raise forms.ValidationError("Correo o contraseña incorrectos")
                self.user = user
            except User.DoesNotExist:
                raise forms.ValidationError("Correo o contraseña incorrectos")
        return cleaned_data
    
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    profesion = forms.CharField(max_length=100, required=False, label="Profesión")
    avatar = forms.ImageField(required=False, label="Foto de perfil")

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
    
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput,
        error_messages={
            "password_mismatch": "Las contraseñas no coinciden.",
        }
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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

class EditUserForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Usuario')
    email = forms.EmailField(required=True, label='Correo electrónico')
    profesion = forms.CharField(label="Profesión", required=False)
    password1 = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirmar contraseña", strip=False, widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("instance", None)
        super().__init__(*args, instance=self.user, **kwargs)

        avatar = Avatar.objects.filter(user=self.user).first()
        if avatar:
            self.fields["profesion"].initial = avatar.profesion

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError("Ese nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("Ese correo electrónico ya está en uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")

        if password1:
            user.set_password(password1)

        if commit:
            user.save()

            profesion = self.cleaned_data.get("profesion")
            avatar, created = Avatar.objects.get_or_create(user=user)
            avatar.profesion = profesion
            avatar.save()

        return user

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if Estudiante.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un estudiante con este correo.")
        return email

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido', 'email', 'profesion']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Profesor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
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
        
        if not self.instance.pk:
            if fecha < datetime.date.today():
                raise forms.ValidationError("La fecha de entrega no puede ser en el pasado.")
        return fecha
    
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']