# Generated by Django 4.2.9 on 2024-01-25 07:45

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0010_remove_question_resource_remove_solution_resource_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='solutionresource',
            name='solution',
            field=tinymce.models.HTMLField(),
        ),
    ]
