# Generated by Django 5.2.3 on 2025-06-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_event_delete_contactinfo_delete_couple_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='love_story_engagement_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='love_story_first_date_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='love_story_first_meet_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='love_story_proposal_date',
            field=models.DateField(),
        ),
    ]
