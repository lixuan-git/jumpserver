# Generated by Django 4.1.13 on 2024-07-29 02:25

import common.db.fields
import common.db.models
from django.conf import settings
from django.db import migrations, models
import uuid


def migrate_user_public_and_private_key(apps, schema_editor):
    user_model = apps.get_model('users', 'User')
    users = user_model.objects.all()
    ssh_key_model = apps.get_model('authentication', 'SSHKey')
    db_alias = schema_editor.connection.alias
    for user in users:
        if user.public_key:
            ssh_key_model.objects.using(db_alias).create(
                public_key=user.public_key, private_key=user.private_key, user=user
            )


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_auto_20190729_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSHKey',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('private_key', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Private key')),
                ('public_key', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Public key')),
                ('date_last_used', models.DateTimeField(blank=True, null=True, verbose_name='Date last used')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=common.db.models.CASCADE_SIGNAL_SKIP,
                                           related_name='ssh_keys', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'SSH key',
            },
        ),
        migrations.RunPython(migrate_user_public_and_private_key)
    ]
