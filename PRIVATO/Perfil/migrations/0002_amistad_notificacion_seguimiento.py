# Generated by Django 4.2.7 on 2024-01-13 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amistad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('par_amigos', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username_emisor', models.TextField()),
                ('username_receptor', models.TextField()),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seguimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_seguidor', models.IntegerField()),
                ('id_receptor', models.IntegerField()),
            ],
        ),
    ]