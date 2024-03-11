# Generated by Django 4.2.9 on 2024-03-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_question_custom_question_note_question_visibility'),
        ('Assessment', '0025_remove_assessment_chapters_assessment_chapters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='chapters',
            field=models.ManyToManyField(blank=True, to='core.chapter'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='questions',
            field=models.ManyToManyField(blank=True, to='core.question'),
        ),
    ]
