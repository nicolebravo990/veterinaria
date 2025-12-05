from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import VeterinarioProfile

@login_required
def vetInicio(request):
    return render(request, 'gestorProductos/vetInicio.html')  # Renderiza la plantilla para usuarios normales

def index(request):
    if request.user.is_authenticated:
        if not (request.user.is_superuser or request.user.is_staff):
            return redirect('vet_inicio')  # Redirige a la vista `vetInicio`
    return render(request, 'index.html')  # Los superusuarios y staff acceden al contenido

def login_redirect(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_index')
    # All other users (clients and veterinarians) go to vet_inicio
    return redirect('vet_inicio')

class SignUpView(SuccessMessageMixin,CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "¡Usuario creado exitosamente!"

    def form_valid(self, form):
        response = super().form_valid(form)
        es_veterinario = form.cleaned_data.get('es_veterinario', False)
        VeterinarioProfile.objects.create(user=self.object, es_veterinario=es_veterinario)
        return response

# List all admins (users with is_staff=True)
class AdminListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestorUser/admin_list.html'
    context_object_name = 'admins'

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

# List all clients (users who are not staff or veterinario)
class ClientListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestorUser/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        veterinarios = VeterinarioProfile.objects.filter(es_veterinario=True).values_list('user_id', flat=True)
        return User.objects.filter(is_staff=False).exclude(id__in=veterinarios)

# List all veterinarians
class VeterinarioListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestorUser/veterinario_list.html'
    context_object_name = 'veterinarios'

    def get_queryset(self):
        veterinarios = VeterinarioProfile.objects.filter(es_veterinario=True).values_list('user_id', flat=True)
        return User.objects.filter(id__in=veterinarios)

# Create views for Admin, Client, Veterinario - reuse SignUpView but with role preset
class AdminCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('admin_list')
    success_message = "Administrador creado exitosamente."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_staff = True
        user.save()
        return response

class ClientCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('client_list')
    success_message = "Cliente creado exitosamente."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        # Ensure client is not staff and not veterinarian
        user.is_staff = False
        user.is_superuser = False
        # Remove VeterinarioProfile if exists
        try:
            profile = user.veterinarioprofile
            profile.delete()
        except VeterinarioProfile.DoesNotExist:
            pass
        user.save()
        return response

class VeterinarioCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('veterinario_list')
    success_message = "Veterinario creado exitosamente."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_staff = False
        user.is_superuser = False
        es_veterinario = form.cleaned_data.get('es_veterinario', False)
        VeterinarioProfile.objects.update_or_create(user=user, defaults={'es_veterinario': es_veterinario})
        user.save()
        return response

# Update views (reuse CustomUserChangeForm to handle roles and profile)
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('index')
    success_message = "Usuario actualizado exitosamente."

    def get_success_url(self):
        # Redirect based on user role
        user = self.object
        if user.is_staff:
            return reverse_lazy('admin_list')
        else:
            try:
                perfil = user.veterinarioprofile
                if perfil.es_veterinario:
                    return reverse_lazy('veterinario_list')
            except VeterinarioProfile.DoesNotExist:
                pass
            return reverse_lazy('client_list')

# Delete view for users
class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'gestorUser/user_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        user = self.object
        if user.is_staff:
            return reverse_lazy('admin_list')
        else:
            try:
                perfil = user.veterinarioprofile
                if perfil.es_veterinario:
                    return reverse_lazy('veterinario_list')
            except VeterinarioProfile.DoesNotExist:
                pass
            return reverse_lazy('client_list')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import CitaMedica
from .forms import CitaMedicaForm

@login_required
def gestionar_citas(request):
    citas = CitaMedica.objects.filter(user=request.user).order_by('fecha', 'hora')
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.user = request.user
            try:
                cita.full_clean()  # Model validation to prevent conflicts
                cita.save()
                messages.success(request, "Cita agendada correctamente.")
                return redirect('vet_inicio')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CitaMedicaForm()
    return render(request, 'gestorProductos/vetInicio.html', {'formulario_cita': form, 'citas_usuario': citas})


@login_required
def agendar_cita(request):
    # Clear any messages from other pages to avoid showing irrelevant alerts
    storage = messages.get_messages(request)
    list(storage)  # Consume all messages

    citas = CitaMedica.objects.filter(user=request.user).order_by('fecha', 'hora')
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.user = request.user
            try:
                cita.full_clean()
                cita.save()
                messages.success(request, "Su hora ha sido agendada correctamente.")
                return redirect('agendar_cita')
            except ValidationError as e:
                if 'Ya hay una cita agendada para esa fecha y hora' in str(e):
                    messages.error(request, "No ha sido agendada porque ya hay otra cita a esa hora.")
                else:
                    messages.error(request, str(e))
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CitaMedicaForm()

    return render(request, 'gestorUser/agendar_cita.html', {'formulario_cita': form, 'citas_usuario': citas})

