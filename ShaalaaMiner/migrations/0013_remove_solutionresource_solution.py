# Generated by Django 4.2.9 on 2024-01-25 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0012_alter_solution_solution_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solutionresource',
            name='solution',
        ),
    ]
