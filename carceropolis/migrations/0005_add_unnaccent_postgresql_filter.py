from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations

class Migration(migrations.Migration):
    """Apply PostgreSQL Extension to allow accent incensitive search."""

    dependencies = [
        ('carceropolis', '0004_auto_20180116_1905'),
    ]

    operations = [
        UnaccentExtension(),
    ]
