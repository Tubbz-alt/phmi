# Generated by Django 2.1.5 on 2019-01-17 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("phmi", "0028_auto_20181206_1519")]

    operations = [
        migrations.CreateModel(
            name="ActivityCategoryGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField()),
                ("index", models.IntegerField(default=0)),
            ],
            options={"ordering": ["index"]},
        ),
        migrations.AlterModelOptions(
            name="activity",
            options={
                "ordering": ["activity_category__index"],
                "verbose_name_plural": "Activities",
            },
        ),
        migrations.AddField(
            model_name="activitycategory",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="phmi.ActivityCategoryGroup",
                related_name="categories",
            ),
        ),
    ]
