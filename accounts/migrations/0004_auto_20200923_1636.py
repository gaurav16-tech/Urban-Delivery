# Generated by Django 3.0.3 on 2020-09-23 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_post_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Uploadimage',
            field=models.ImageField(blank=True, null=True, upload_to='static/mechit/images/'),
        ),
    ]