# Generated by Django 3.2.2 on 2021-05-18 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210518_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
        ),
    ]
