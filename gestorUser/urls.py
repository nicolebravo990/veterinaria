from django.urls import path
from gestorUser.views import (
    SignUpView,
    AdminListView, AdminCreateView,
    ClientListView, ClientCreateView,
    VeterinarioListView, VeterinarioCreateView,
    UserUpdateView, UserDeleteView,
    gestionar_citas,
    agendar_cita,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="Signup"),

    # Admin user urls
    path('admin/list/', AdminListView.as_view(), name='admin_list'),
    path('admin/create/', AdminCreateView.as_view(), name='admin_create'),

    # Client user urls
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),

    # Veterinario user urls
    path('veterinario/list/', VeterinarioListView.as_view(), name='veterinario_list'),
    path('veterinario/create/', VeterinarioCreateView.as_view(), name='veterinario_create'),

    # Generic update and delete urls for users (all roles)
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    # Appointment scheduling
    path('citas/', gestionar_citas, name='gestionar_citas'),
    path('citas/agendar/', agendar_cita, name='agendar_cita'),
]





