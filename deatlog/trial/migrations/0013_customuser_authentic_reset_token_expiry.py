# Generated by Django 4.1.3 on 2024-08-09 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trial', '0012_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_token', models.CharField(blank=True, max_length=32, null=True)),
                ('reset_token_expiry', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='authentic',
            name='reset_token_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]