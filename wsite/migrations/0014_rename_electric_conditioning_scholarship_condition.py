# Generated by Django 5.0.1 on 2024-05-20 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wsite', '0013_rename_electric_onditioning_scholarship_electric_conditioning'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scholarship',
            old_name='electric_conditioning',
            new_name='condition',
        ),
    ]