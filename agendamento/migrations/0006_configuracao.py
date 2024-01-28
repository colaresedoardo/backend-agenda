# Generated by Django 5.0.1 on 2024-01-28 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0005_evento_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador_whatsapp_business', models.CharField(default='', max_length=200, null=True)),
                ('intervalo_entre_horario', models.IntegerField(default=30, max_length=10, null=True)),
                ('horario_inicial', models.TimeField(null=True)),
                ('horario_final', models.TimeField(null=True)),
            ],
        ),
    ]