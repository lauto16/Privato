# Generated by Django 4.2.7 on 2024-01-14 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0004_remove_notificacion_username_receptor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='id_emisor',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
