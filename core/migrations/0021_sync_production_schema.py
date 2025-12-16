from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_remove_weddingevent_venue_address_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WeddingGift",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("gift_type", models.CharField(
                    choices=[
                        ("money", "Money Transfer"),
                        ("bank", "Bank Transfer"),
                        ("registry", "Registry"),
                        ("other", "Other"),
                    ],
                    default="money",
                    max_length=20,
                )),
                ("provider", models.CharField(
                    blank=True,
                    help_text="Provider name e.g., Airtel Money",
                    max_length=100,
                    null=True,
                )),
                ("account_name", models.CharField(
                    blank=True,
                    help_text="Account or recipient name",
                    max_length=255,
                    null=True,
                )),
                ("account_number", models.CharField(
                    blank=True,
                    help_text="Phone number / account number",
                    max_length=100,
                    null=True,
                )),
                ("instructions", models.TextField(
                    blank=True,
                    help_text="Any instructions for the contribution",
                    null=True,
                )),
                ("url", models.URLField(
                    blank=True,
                    help_text="Optional link (e.g., registry link)",
                    null=True,
                )),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("wedding", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="gifts",
                    to="core.weddingevent",
                )),
            ],
            options={
                "verbose_name": "Wedding Gift",
                "verbose_name_plural": "Wedding Gifts",
                "ordering": ["order", "id"],
            },
        ),
    ]
