# Generated by Django 4.2.9 on 2024-01-25 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0004_subject_chapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.URLField()),
                ('meta', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SolutionResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.URLField()),
                ('meta', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField()),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.questionresource')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('url', models.URLField()),
                ('solution_url', models.URLField()),
                ('review_required', models.BooleanField(default=False)),
                ('meta', models.CharField(max_length=500)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.chapter')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.questionresource')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.solution')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.questiontype')),
            ],
        ),
    ]
