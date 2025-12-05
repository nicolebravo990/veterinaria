from django import forms
from .models import CitaMedica
from django.forms.widgets import DateInput, TimeInput

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['mascota', 'tipo_mascota', 'titular', 'fecha', 'hora', 'motivo']
        labels = {
            'mascota': 'Nombre de Mascota',
        }
        widgets = {
            'mascota': forms.TextInput(attrs={'class': 'form-control', 'readonly': False}),
            'tipo_mascota': forms.Select(attrs={'class': 'form-select', 'disabled': False}),
            'titular': forms.TextInput(attrs={'class': 'form-control', 'readonly': False}),
            'fecha': DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': False}),
            'hora': TimeInput(attrs={'type': 'time', 'class': 'form-control', 'readonly': False}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'readonly': False}),
        }
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import VeterinarioProfile

class CustomUserCreationForm(UserCreationForm):
    es_veterinario = forms.BooleanField(required=False, label='Registrarse como veterinario')
    is_staff = forms.BooleanField(required=False, label='Registrar como admin (staff)')
    is_superuser = forms.BooleanField(required=False, label='Registrar como superusuario')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'es_veterinario', 'is_staff', 'is_superuser')

class CustomUserChangeForm(UserChangeForm):
    es_veterinario = forms.BooleanField(required=False, label='Es veterinario')
    is_staff = forms.BooleanField(required=False, label='Es admin (staff)')
    is_superuser = forms.BooleanField(required=False, label='Es superusuario')

    class Meta:
        model = User
        fields = ('username', 'email', 'es_veterinario', 'is_staff', 'is_superuser', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value for es_veterinario from related VeterinarioProfile
        if self.instance and hasattr(self.instance, 'veterinarioprofile'):
            self.fields['es_veterinario'].initial = self.instance.veterinarioprofile.es_veterinario
        else:
            self.fields['es_veterinario'].initial = False

    def save(self, commit=True):
        user = super().save(commit=False)
        es_veterinario = self.cleaned_data.get('es_veterinario', False)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        if commit:
            user.save()
            # Update or create VeterinarioProfile accordingly
            if es_veterinario:
                VeterinarioProfile.objects.update_or_create(user=user, defaults={'es_veterinario': True})
            else:
                # If profile exists and es_veterinario=False, delete the profile
                try:
                    profile = user.veterinarioprofile
                    profile.delete()
                except VeterinarioProfile.DoesNotExist:
                    pass
        return user

class VeterinarioProfileForm(forms.ModelForm):
    class Meta:
        model = VeterinarioProfile
        fields = ('es_veterinario',)
