from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models.signals import post_save , pre_save
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime


CATEGORY_CHOICES = (
    ('HF', 'Hot Food'),
    ('CF', 'Cold Food'),
    ('S', 'Snacks'),
    ('F', 'Frozen'),
    ('D', 'Drink'),
)

BREAK_CHOICES =(
    ('T', 'Morning Tea'),
    ('L', 'Lunch')
)

PAYMENT_CHOICES = (
    ('B', 'Pay with Card (Credit/Debit)'),
    ('C', 'Pay with Cash at Tuck Shop')
)


# Model for 'closed' dates
class ClosedDate(models.Model):
    closed_dates = models.DateField(unique=True)


# Model for current window using closed dates to determine next open day
# class CurrentWindow(models.Model):
#     Open = models.BooleanField(default=True)
# 
#     def open_check(self, *args, **kwargs):
#         time = CutoffTime.objects.get()
#         cuttime = time.cutoff
#         now = datetime.datetime.now().time()
#         self.today = datetime.date.today()
# 
#         self.Open = True
#         if now > cuttime:
#             self.today = self.today + datetime.timedelta(days=1)
#        
#        self.today 
#         else:
#             try:
#                 check = ClosedDate.objects.filter(closed_dates=today)
#                 if check.exists():
#                     self.Open = False
#             except ObjectDoesNotExist:
#                 self.Open = True
# 
#     def save(self, *args, **kwargs):
#         if not self.pk and CutoffTime.objects.exists():
#             # if you'll not check for self.pk
#             # then error will also raised if cut off time already exists
#             raise ValidationError('There is can be only one Cut off time instance')
#         return super(CutoffTime, self).save(*args, **kwargs)

# model for daily cut off time
class CutoffTime(models.Model):
    class Meta:
        verbose_name = 'Cutoff Time'
        verbose_name_plural = 'Cutoff Time'
    cutoff = models.TimeField(default=datetime.time(hour=9, minute=0, second=0, microsecond=0))

    def save(self, *args, **kwargs):
        if not self.pk and CutoffTime.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised if cut off time already exists
            raise ValidationError('There is can be only one Cut off time instance')
        return super(CutoffTime, self).save(*args, **kwargs)


''' User Profile Data '''


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(default='', max_length=100)
    lastname = models.CharField(default='', max_length=100)
    user_email = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.user.username

    def save(self , *args , **kwargs):
        email_address = self.user.email
        self.user_email = email_address
        self.firstname = self.user.first_name
        self.lastname = self.user.last_name
        super().save(*args, **kwargs)


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    if instance.email != '' and not instance.username:
        user_email = instance.email
        username = user_email[:30].split("@")[0]

        instance.username = username


# Item model


class Item(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Menu'
    title = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=4, blank=False, null=False)
    discount_price = models.DecimalField(decimal_places=2,blank=True, null=True, max_digits=4)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField(default='', editable=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/images/', default='media/images/no-image-available-icon-template-260nw'
                                                                 '-1036735678.jpg_xctPfVt.png') 
    maximum_quantity = models.IntegerField(default=10)
    not_available = models.BooleanField(default=False)
    variations_exist = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def save(self , *args , **kwargs):  # save method overide
        if not self.slug:
            value = self.title
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        if ItemVariation.objects.filter(item=self).exists():
            self.variations_exist = True
        else:
            self.variations_exist = False
        super().save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def select_option_url(self):
        return reverse("core:select-option", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class ItemVariation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # deletes Item variation when item is deleted
    variation = models.CharField(max_length=30)  # e.g. flavour or volume (for drinks)
    price = models.DecimalField("Price (if different from base price)", decimal_places=2, max_digits=4, null=True, blank=True)
    # discount_price = models.DecimalField(decimal_places=2 , blank=True , null=True , max_digits=4)
    image = models.ImageField(upload_to='media/images/' ,
                              default='media/images/no-image-available-icon-template-260nw-1036735678.jpg_xctPfVt.png')
    slug = models.SlugField(default='')
    not_available = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            'variation', 'price'
        )

    def __str__(self):
        return self.item.title + ' (' + self.variation + ')'

    def save(self , *args , **kwargs):
        value = (self.item.title + '-' + self.variation)
        self.slug = slugify(value , allow_unicode=True)

        # if not self.discount_price:
        #     self.discount_price = self.item.discount_price
        if not self.price:
            self.price = self.item.price
        super().save(*args, **kwargs)
        if ItemVariation.objects.filter(item=self.item).exists():
            self.item.variations_exist = True
        else:
            self.item.variations_exist = False
        self.item.save(*args, **kwargs)

    def delete(self, *args , **kwargs):
        super().delete(*args , **kwargs)
        if ItemVariation.objects.filter(item=self.item).exists():
            self.item.variations_exist = True
        else:
            self.item.variations_exist = False
        self.item.save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    title = models.CharField(default='', max_length=20)
    price = models.DecimalField(default=0.00, decimal_places=2 , max_digits=4)
    slug = models.SlugField(default='')

    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True) # sets field to null to protect model
    item_variations = models.ForeignKey(ItemVariation, on_delete=models.SET_NULL, null=True)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.title}"

    def save(self, *args, **kwargs):
        if self.item_variations:
            self.title = str(self.item.title + ' (' + self.item_variations.variation + ')')
            self.price = self.item_variations.price
            self.slug = self.item_variations.slug
        elif self.item:
            self.title = self.item.title
            self.price = self.item.price
            self.slug = self.item.slug
        super().save(*args , **kwargs)

    def get_total_item_price(self):
        if not self.item_variations:
            return self.quantity * self.item.price
        elif self.item_variations:
            return self.quantity * self.item_variations.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem, related_name='orderitem')
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    pickup_date = models.DateField("Pickup Date", default=datetime.date.today)
    break_choice = models.CharField(choices=BREAK_CHOICES, default='T', max_length=20)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='B')
    order_total = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)
    # coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)


    '''
    1. Item added to cart
    2. Add pickup date
    3. add pickup time
    '''

    def set_window(self):  # currently unused, will create proper method later
        today = datetime.date.today()
        current_window = today

        next_window = order_window = datetime.date.today() + datetime.timedelta(days=1)
        time = CutoffTime.objects.get()
        cuttime = time.cutoff
        now = datetime.datetime.now().time()
        if now <= cuttime:
            order_window = current_window
        elif now > cuttime:
            order_window = next_window
        self.pickup_date = order_window

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        self.order_total = total
        return total

    def get_add_order_to_cart_url(self):
        return reverse("core:add-order-to-cart", kwargs={
            'ref_code': self.ref_code
        })

    def delete(self, *args , **kwargs):
        net_order = NetOrders.objects.get(
            date=self.pickup_date
        )
        for order_item in self.items.all():
            net_item = NetItem.objects.get(
                date=net_order ,
                slug=order_item.slug ,
                title=order_item.title ,
            )
            net_item.quantity -= order_item.quantity
            if net_item.quantity<=0:
                net_item.delete()
            else:
                net_item.save()
        super().delete(*args , **kwargs)




class NetOrders(models.Model):
    class Meta:
        verbose_name = 'Net Orders'
        verbose_name_plural = 'Net Orders'
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.date)


class NetItem(models.Model):
    date = models.ForeignKey(NetOrders, on_delete=models.CASCADE)
    title = models.CharField(default='' , max_length=20)
    slug = models.SlugField(default='')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# class Coupon(models.Model):
#     code = models.CharField(max_length=15)
#     amount = models.FloatField()
#
#     def __str__(self):
#         return self.code
#
