# Generated by Django 3.2.7 on 2021-09-14 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_auto_20210914_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='project_jobs', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='job',
            name='staff_id',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_jobs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]