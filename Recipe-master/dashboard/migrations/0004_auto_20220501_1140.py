# Generated by Django 3.2.6 on 2022-05-01 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_recipe_rating_points'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='rating_points',
            new_name='no_of_user_rated_points_1',
        ),
        migrations.AddField(
            model_name='recipe',
            name='no_of_user_rated_points_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='no_of_user_rated_points_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='no_of_user_rated_points_4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='no_of_user_rated_points_5',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='rating_points_avg',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
