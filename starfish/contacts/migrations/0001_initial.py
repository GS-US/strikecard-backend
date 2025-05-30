# Generated by Django 5.2 on 2025-05-29 18:42

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chapters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashedContactRecord',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                (
                    'email_hash',
                    models.CharField(db_index=True, editable=False, max_length=128),
                ),
                (
                    'phone_hash',
                    models.CharField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        max_length=128,
                        null=True,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseContact',
            fields=[
                (
                    'hashedcontactrecord_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='contacts.hashedcontactrecord',
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                (
                    'referer_full',
                    models.TextField(blank=True, null=True, verbose_name='Referrer'),
                ),
                (
                    'referer_host',
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                'ordering': ('-created',),
            },
            bases=('contacts.hashedcontactrecord',),
        ),
        migrations.CreateModel(
            name='ExpungedContact',
            fields=[
                (
                    'hashedcontactrecord_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='contacts.hashedcontactrecord',
                    ),
                ),
                ('validated', models.DateTimeField()),
                ('expunged', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('contacts.hashedcontactrecord',),
        ),
        migrations.CreateModel(
            name='RemovedContact',
            fields=[
                (
                    'hashedcontactrecord_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='contacts.hashedcontactrecord',
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('unsubscribed', 'Unsubscribed'),
                            ('deleted', 'Deleted'),
                            ('bounced', 'Bounced'),
                        ],
                        max_length=20,
                    ),
                ),
                ('removed', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('contacts.hashedcontactrecord',),
        ),
        migrations.CreateModel(
            name='HistoricalContact',
            fields=[
                (
                    'basecontact_ptr',
                    models.ForeignKey(
                        auto_created=True,
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        related_name='+',
                        to='contacts.basecontact',
                    ),
                ),
                (
                    'hashedcontactrecord_ptr',
                    models.ForeignKey(
                        auto_created=True,
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        related_name='+',
                        to='contacts.hashedcontactrecord',
                    ),
                ),
                (
                    'id',
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name='ID'
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                (
                    'email_hash',
                    models.CharField(db_index=True, editable=False, max_length=128),
                ),
                (
                    'phone_hash',
                    models.CharField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        max_length=128,
                        null=True,
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                (
                    'referer_full',
                    models.TextField(blank=True, null=True, verbose_name='Referrer'),
                ),
                (
                    'referer_host',
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ('validated', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                (
                    'history_type',
                    models.CharField(
                        choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')],
                        max_length=1,
                    ),
                ),
                (
                    'chapter',
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='+',
                        to='chapters.chapter',
                    ),
                ),
            ],
            options={
                'verbose_name': 'historical contact',
                'verbose_name_plural': 'historical contacts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
