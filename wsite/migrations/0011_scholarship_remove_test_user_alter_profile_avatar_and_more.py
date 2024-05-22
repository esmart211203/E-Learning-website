# Generated by Django 5.0.1 on 2024-05-20 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsite', '0010_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('number_of_slots', models.IntegerField()),
                ('scholarship_value', models.CharField(max_length=255)),
                ('electric_onditioning', models.CharField(max_length=255)),
                ('form', models.CharField(max_length=255)),
                ('image', models.ImageField(max_length=255, upload_to='scholarship')),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='profile'),
        ),
        migrations.AlterField(
            model_name='subimages',
            name='image',
            field=models.ImageField(max_length=255, upload_to='subimages'),
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]