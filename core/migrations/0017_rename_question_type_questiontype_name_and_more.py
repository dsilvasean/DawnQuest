# Generated by Django 4.2.9 on 2024-02-03 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_type_subtype_question_subtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questiontype',
            old_name='question_type',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subtype',
        ),
        migrations.AddField(
            model_name='questiontype',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.questiontype'),
        ),
        migrations.DeleteModel(
            name='QuestionSubType',
        ),
    ]
