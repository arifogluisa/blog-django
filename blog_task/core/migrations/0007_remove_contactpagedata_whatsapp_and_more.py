# Generated by Django 4.1.2 on 2022-10-22 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_contact_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactpagedata',
            name='whatsapp',
        ),
        migrations.AddField(
            model_name='contactpagedata',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='contactpagedata',
            name='contact',
            field=models.TextField(blank=True, null=True, verbose_name='contact'),
        ),
    ]