# Generated by Django 5.2 on 2025-04-12 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0002_auditlog"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLogInventory",
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
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("CREATE", "Create"),
                            ("UPDATE", "Update"),
                            ("DELETE", "Delete"),
                        ],
                        max_length=10,
                    ),
                ),
                ("model_name", models.CharField(max_length=100)),
                ("object_id", models.PositiveIntegerField()),
                ("description", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.company"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleInventory",
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
                ("brand", models.CharField(max_length=40)),
                ("model", models.CharField(max_length=40)),
                ("year", models.IntegerField()),
                (
                    "fuel_type",
                    models.CharField(
                        choices=[
                            ("PETROL", "Petrol"),
                            ("DIESEL", " Diesel"),
                            ("ELECTRIC", "Electric"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "transmission",
                    models.CharField(
                        choices=[
                            ("ELECTRIC", "Electric"),
                            ("MANUAL", "Manual"),
                            ("AUTOMATIC", "Automatic"),
                        ],
                        max_length=20,
                    ),
                ),
                ("price", models.IntegerField()),
                ("quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("modified_at", models.DateTimeField(auto_now_add=True)),
                ("mileage", models.IntegerField()),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inventory",
                        to="users.company",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
