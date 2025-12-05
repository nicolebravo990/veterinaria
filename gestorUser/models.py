from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class CitaMedica(models.Model):
    TIPO_MASCOTA_CHOICES = [
        ('gato', 'Gato'),
        ('perro', 'Perro'),
        ('ave', 'Ave'),
        ('conejo', 'Conejo'),
        ('hamster', 'Hamster'),
        ('otro', 'Otro'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="citas")
    mascota = models.CharField(max_length=100, verbose_name='Nombre de Mascota')
    tipo_mascota = models.CharField(max_length=10, choices=TIPO_MASCOTA_CHOICES, default='otro', verbose_name='Tipo de Mascota')
    titular = models.CharField(max_length=100, blank=True, null=True)  # Owner's name
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(blank=True, null=True)

    class Meta:
        pass

    def clean(self):
        # Check if appointment datetime is in the past
        cita_datetime = timezone.make_aware(timezone.datetime.combine(self.fecha, self.hora))
        if cita_datetime < timezone.now():
            raise ValidationError("No se puede agendar una cita en el pasado.")

        # Check for overlapping appointments globally
        overlapping = CitaMedica.objects.filter(fecha=self.fecha, hora=self.hora).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("Ya hay una cita agendada para esa fecha y hora.")

    def __str__(self):
        return f"Cita de {self.mascota} con {self.user.username} el {self.fecha} a las {self.hora}"
from django.contrib.auth.models import User

class VeterinarioProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    es_veterinario = models.BooleanField(default=False)

    def __str__(self):
        return f"Veterinario profile for {self.user.username} - Veterinario: {self.es_veterinario}"
