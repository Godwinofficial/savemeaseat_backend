from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='invitations_done',
            field=models.BooleanField(default=False, help_text='When true, invitations are marked done and further invitations should be blocked.'),
        ),
    ]
