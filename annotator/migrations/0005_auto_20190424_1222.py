# Generated by Django 2.1.7 on 2019-04-24 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotator', '0004_auto_20190423_1123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labeleddata',
            old_name='predicted_e1',
            new_name='e1',
        ),
        migrations.RenameField(
            model_name='labeleddata',
            old_name='predicted_e2',
            new_name='e2',
        ),
        migrations.RemoveField(
            model_name='labeleddata',
            name='predicted_e1_end',
        ),
        migrations.RemoveField(
            model_name='labeleddata',
            name='predicted_e1_start',
        ),
        migrations.RemoveField(
            model_name='labeleddata',
            name='predicted_e2_end',
        ),
        migrations.RemoveField(
            model_name='labeleddata',
            name='predicted_e2_start',
        ),
        migrations.AddField(
            model_name='labeleddata',
            name='e1_end',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='labeleddata',
            name='e1_start',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='labeleddata',
            name='e2_end',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='labeleddata',
            name='e2_start',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='unlabeleddata',
            name='e1_end',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='unlabeleddata',
            name='e1_start',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='unlabeleddata',
            name='e2_end',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='unlabeleddata',
            name='e2_start',
            field=models.IntegerField(default=-1),
        ),
    ]
