from bson import ObjectId
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def generate_unique_object_id():
    return str(ObjectId())


class ProductType:
    MEMBERSHIP = 'MM'

    CHOICES = (
        (MEMBERSHIP, 'MEMBERSHIP {}'.format(MEMBERSHIP)),
    )


class DurationType:
    DAY = 'D'
    YEAR = 'Y'
    MONTH = 'M'

    CHOICES = (
        (DAY, 'DAY  {}'.format(DAY)),
        (YEAR, 'YEAR  {}'.format(YEAR)),
        (MONTH, 'MONTH  {}'.format(MONTH)),
    )


class OrderSource:
    APP = 'A'
    WEB = 'I'

    CHOICES = (
        (APP, 'ANDROID {}'.format(APP)),
        (WEB, 'IOS {}'.format(WEB))
    )


class PaymentStatus:
    PENDING = "PENDING"
    COMPLETED = 'COMPLETED'
    PARTIAL = "PARTIAL"
    REFUNDED = "REFUNDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    CHOICES = (
        (PENDING, 'PENDING'),
        (COMPLETED, 'COMPLETED'),
        (PARTIAL, 'PARTIAL'),
        (REFUNDED, 'REFUNDED'),
        (FAILED, 'FAILED'),
        (CANCELLED, 'CANCELLED'),
    )


class PaymentProvider:
    PLAY_STORE = 'PS'
    IPHONE_APP_STORE = 'IS'

    CHOICES = (
        (PLAY_STORE, 'PLAY_STORE'),
        (IPHONE_APP_STORE, 'IPHONE_APP_STORE'),
    )


class OrderStatus:
    PENDING = 'PE'
    COMPLETED = 'CO'
    FAILED = 'FL'

    CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed')
    )


class SubscriptionType:
    PAID = 'P'
    TRIAL = 'T'
    CHOICES = (
        (PAID, 'PAID:{}'.format(PAID)),
        (TRIAL, 'TRIAL:{}'.format(TRIAL))
    )


class Membership(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    title = models.CharField(max_length=500)
    actual_price = models.FloatField(default=0, validators=[MinValueValidator(1.0), ],
                                     help_text='Enter Price in Dollars')

    duration_type = models.CharField(choices=DurationType.CHOICES, max_length=1)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1.0), ], default=1)

    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'C1.Membership'

    def __str__(self):
        return self.title

    @staticmethod
    def get_membership_by_id(membership_id):
        try:
            return Membership.objects.get(id=membership_id)
        except Membership.DoesNotExist:
            return None


class Order(models.Model):
    id = models.CharField(default=generate_unique_object_id, max_length=24, primary_key=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    item_type = models.CharField(choices=ProductType.CHOICES, max_length=2)
    item_id = models.CharField(max_length=24, db_index=True)
    email = models.EmailField(max_length=500)

    order_source = models.CharField(choices=OrderSource.CHOICES, max_length=1)
    payment_provider = models.CharField(max_length=2, choices=PaymentProvider.CHOICES)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.CHOICES,
                                      default=PaymentStatus.PENDING)

    # payu_id = models.CharField(max_length=50, blank=True, null=True)  # for PayU
    payment_id = models.CharField(max_length=50, blank=True, null=True)

    item_price = models.FloatField(default=0)
    # discount_price_applied = models.FloatField(default=0)
    payable_amount = models.FloatField(default=0)  # payable_amount = item_price - discount_price_applied

    amount_paid = models.FloatField(default=0)
    is_total_amount_paid = models.BooleanField(default=False)
    additional_charges = models.FloatField(default=0)

    detail = models.CharField(max_length=500, blank=True, null=True)
    # receipt_no = models.CharField(max_length=50)

    order_status = models.CharField(max_length=2, choices=OrderStatus.CHOICES, default=OrderStatus.PENDING)
    recreate_subscription = models.BooleanField(default=False)

    #: response returned to android/ios after payment
    response_json = models.TextField()

    is_picked_by_payment_recheck_job = models.BooleanField(default=False)
    # payment recheck response after validating payment
    payment_recheck_details = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now, db_index=True)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    class Meta:
        ordering = ['created_on']
        verbose_name_plural = 'A. Orders'


class UserMembership(models.Model):
    id = models.CharField(default=generate_unique_object_id, primary_key=True, max_length=24)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # to keep reference of what package user had subscribed
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, blank=True, null=True)
    end_date_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    #: to get proper info if users are accessing premium content in trial period or they have
    #  purchased to show proper message
    subscription_type = models.CharField(choices=SubscriptionType.CHOICES, max_length=1)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'C2.UserMembership'

    @staticmethod
    def get_user_membership_by_user_id(user_id):
        try:
            return UserMembership.objects.get(user_id=user_id)
        except UserMembership.DoesNotExist:
            return None

    @staticmethod
    def is_trial_period_allowed(user_id):
        return not UserMembership.objects.filter(user_id=user_id).exists()
