# Generated by Django 5.0.1 on 2024-01-28 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0003_alter_servico_descricao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='evento',
            name='titulo',
        ),
        migrations.AddField(
            model_name='evento',
            name='horario',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_fim',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_inicio',
            field=models.DateField(null=True),
        ),
    ]
