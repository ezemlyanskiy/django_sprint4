# Generated by Django 3.2.16 on 2024-02-11 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_comment_ordering_verbose_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('pub_date',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_at',
            new_name='pub_date',
        ),
    ]