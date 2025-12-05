# Generated manually to add CitaMedica model migration

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('gestorUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitaMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mascota', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('motivo', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='auth.user')),
            ],
            options={
                'unique_together': {('fecha', 'hora')},
            },
        ),
    ]
