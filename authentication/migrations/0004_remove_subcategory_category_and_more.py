# Generated by Django 5.1.1 on 2024-11-17 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_category_subcategory_servicesession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='servicesession',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='ServiceSession',
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
    ]