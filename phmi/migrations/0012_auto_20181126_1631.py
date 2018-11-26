# Generated by Django 2.1.2 on 2018-11-26 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phmi', '0011_auto_20181108_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legalmapping',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='legalmapping',
            name='justification',
        ),
        migrations.RemoveField(
            model_name='legalmapping',
            name='org_type',
        ),
        migrations.RemoveField(
            model_name='orgtype',
            name='activities',
        ),
        migrations.AddField(
            model_name='legaljustification',
            name='activites',
            field=models.ManyToManyField(to='phmi.Activity'),
        ),
        migrations.AddField(
            model_name='legaljustification',
            name='org_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='phmi.OrgType'),
        ),
        migrations.AddField(
            model_name='legaljustification',
            name='statute',
            field=models.TextField(default='', unique=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='duty_of_confidence',
            field=models.CharField(blank=True, choices=[('Implied consent/reasonable expectations', 'Implied consent/reasonable expectations'), ('Set aside as data will be de-identified for this purpose', 'Set aside as data will be de-identified for this purpose')], default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='legaljustification',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='legaljustification',
            unique_together={('name', 'org_type')},
        ),
        migrations.DeleteModel(
            name='LegalMapping',
        ),
    ]
