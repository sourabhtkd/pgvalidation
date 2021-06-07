# Generated by Django 3.2.4 on 2021-06-07 09:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.CharField(default=website.models.generate_unique_object_id, max_length=24, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('actual_price', models.FloatField(default=0, help_text='Enter Price in Dollars', validators=[django.core.validators.MinValueValidator(1.0)])),
                ('duration_type', models.CharField(choices=[('D', 'DAY  D'), ('Y', 'YEAR  Y'), ('M', 'MONTH  M')], max_length=1)),
                ('duration', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'C1.Membership',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(default=website.models.generate_unique_object_id, max_length=24, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('item_type', models.CharField(choices=[('MM', 'MEMBERSHIP MM')], max_length=2)),
                ('item_id', models.CharField(db_index=True, max_length=24)),
                ('email', models.EmailField(max_length=500)),
                ('order_source', models.CharField(choices=[('A', 'ANDROID A'), ('I', 'IOS I')], max_length=1)),
                ('payment_provider', models.CharField(choices=[('PS', 'PLAY_STORE'), ('IS', 'IPHONE_APP_STORE')], max_length=2)),
                ('payment_status', models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('PARTIAL', 'PARTIAL'), ('REFUNDED', 'REFUNDED'), ('FAILED', 'FAILED'), ('CANCELLED', 'CANCELLED')], default='PENDING', max_length=10)),
                ('payment_id', models.CharField(blank=True, max_length=50, null=True)),
                ('item_price', models.FloatField(default=0)),
                ('payable_amount', models.FloatField(default=0)),
                ('amount_paid', models.FloatField(default=0)),
                ('is_total_amount_paid', models.BooleanField(default=False)),
                ('additional_charges', models.FloatField(default=0)),
                ('detail', models.CharField(blank=True, max_length=500, null=True)),
                ('order_status', models.CharField(choices=[('PE', 'Pending'), ('CO', 'Completed'), ('FL', 'Failed')], default='PE', max_length=2)),
                ('recreate_subscription', models.BooleanField(default=False)),
                ('response_json', models.TextField()),
                ('is_picked_by_payment_recheck_job', models.BooleanField(default=False)),
                ('payment_recheck_details', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'A. Orders',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.CharField(default=website.models.generate_unique_object_id, max_length=24, primary_key=True, serialize=False)),
                ('end_date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('subscription_type', models.CharField(choices=[('P', 'PAID:P'), ('T', 'TRIAL:T')], max_length=1)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('membership', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'C2.UserMembership',
            },
        ),
    ]
