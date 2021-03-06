# Generated by Django 2.1.5 on 2019-02-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("phmi", "0037_add_datamap_services_and_service")]

    operations = [
        migrations.AlterModelOptions(
            name="activity",
            options={
                "ordering": ["activity_category__index", "name"],
                "verbose_name_plural": "Activities",
            },
        ),
        migrations.AddField(
            model_name="legaljustification",
            name="org_types",
            field=models.ManyToManyField(blank=True, to="phmi.OrgType"),
        ),
        migrations.AlterField(
            model_name="legaljustification",
            name="name",
            field=models.TextField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="legaljustification", unique_together=set()
        ),
        migrations.RemoveField(model_name="legaljustification", name="org_type"),
    ]
