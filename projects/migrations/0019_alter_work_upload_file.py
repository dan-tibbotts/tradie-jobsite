# Generated by Django 3.2.7 on 2021-09-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_alter_work_upload_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='upload_file',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
