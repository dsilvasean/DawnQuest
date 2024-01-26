# Generated by Django 4.2.9 on 2024-01-25 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0015_question_solution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='solution',
        ),
        migrations.AddField(
            model_name='solution',
            name='question',
            field=models.ForeignKey(default=821, on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solutionresource',
            name='solution',
            field=models.ForeignKey(default=614, on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.solution'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='solution_url',
            field=models.URLField(max_length=555),
        ),
    ]
