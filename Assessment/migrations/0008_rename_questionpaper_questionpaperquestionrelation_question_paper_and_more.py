# Generated by Django 4.2.9 on 2024-02-02 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Assessment', '0007_questionpaper_questions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionpaperquestionrelation',
            old_name='questionpaper',
            new_name='question_paper',
        ),
        migrations.RenameField(
            model_name='questionpaperquestionrelation',
            old_name='questionpaperquestion',
            new_name='question_paper_question',
        ),
    ]