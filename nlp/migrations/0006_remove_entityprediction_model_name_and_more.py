# Generated by Django 5.2.4 on 2025-07-29 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nlp", "0005_alter_entityprediction_model_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="entityprediction",
            name="model_name",
        ),
        migrations.RemoveField(
            model_name="entityprediction",
            name="model_version",
        ),
    ]
