# Generated by Django 4.0.4 on 2022-04-15 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_alter_user_phone_alter_user_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(),
        ),
    ]