# Generated by Django 5.1.2 on 2024-10-30 20:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.CharField(max_length=100),
        ),
    ]
