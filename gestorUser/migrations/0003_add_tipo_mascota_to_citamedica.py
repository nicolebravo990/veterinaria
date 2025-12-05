# Generated migration to add tipo_mascota field to CitaMedica

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('gestorUser', '0002_add_citamedica'),
    ]

    operations = [
        migrations.AddField(
            model_name='citamedica',
            name='tipo_mascota',
            field=models.CharField(
                choices=[('gato', 'Gato'), ('perro', 'Perro'), ('otro', 'Otro')],
                default='otro',
                max_length=10
            ),
        ),
    ]
