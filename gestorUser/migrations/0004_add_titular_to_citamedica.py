# Generated migration to add titular field to CitaMedica

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('gestorUser', '0003_add_tipo_mascota_to_citamedica'),
    ]

    operations = [
        migrations.AddField(
            model_name='citamedica',
            name='titular',
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True
            ),
        ),
    ]
