# Generated by Django 5.1.6 on 2025-02-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_questionanswers_is_answered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Started At'),
        ),
    ]
