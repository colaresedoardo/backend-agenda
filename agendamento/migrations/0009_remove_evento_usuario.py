# Generated by Django 5.0.1 on 2024-02-03 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0008_configuracao_horario_final_sabado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='usuario',
        ),
    ]
