# Generated by Django 4.2.7 on 2024-01-18 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0008_delete_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('contenido', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
