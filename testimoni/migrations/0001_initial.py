# Generated by Django 5.1.3 on 2024-11-18 02:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Testimoni",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subkategori", models.CharField(max_length=100)),
                ("sesi_layanan", models.CharField(max_length=100)),
                ("nama_pekerja", models.CharField(max_length=100)),
                ("rating", models.IntegerField()),
                ("komentar", models.TextField()),
                ("tanggal", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
