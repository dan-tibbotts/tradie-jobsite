# Generated by Django 3.2.7 on 2021-09-14 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210914_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_jobs', to='projects.project'),
        ),
    ]
