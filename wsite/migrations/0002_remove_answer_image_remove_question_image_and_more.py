# Generated by Django 5.0.1 on 2024-05-14 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='question',
            name='_class',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='wsite.class'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='wsite.subject'),
        ),
        migrations.CreateModel(
            name='SubImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=255, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wsite.answer')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wsite.question')),
            ],
        ),
    ]
