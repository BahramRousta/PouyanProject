# Generated by Django 4.2.1 on 2023-05-14 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_remove_post_comment'),
        ('comment', '0002_alter_comment_options_rename_text_comment_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.post'),
            preserve_default=False,
        ),
    ]
