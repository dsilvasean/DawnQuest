# Generated by Django 4.2.9 on 2024-01-25 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0009_alter_question_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='resource',
        ),
        migrations.AddField(
            model_name='questionresource',
            name='question',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solutionresource',
            name='solution',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.solution'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='meta',
            field=models.CharField(max_length=255),
        ),
    ]
