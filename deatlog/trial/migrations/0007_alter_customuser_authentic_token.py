# Generated by Django 4.1.3 on 2024-08-09 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trial', '0006_customuser_authentic_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='authentic_token',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='trial.authentic'),
        ),
    ]
