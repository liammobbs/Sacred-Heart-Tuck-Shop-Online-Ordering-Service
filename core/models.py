from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils.text import slugify
# from django_countries.fields import CountryField
from django.utils import timezone
import datetime


CATEGORY_CHOICES = (
    ('HF', 'Hot Food'),
    ('CF', 'Cold Food'),
    ('S', 'Snacks'),
    ('F', 'Frozen'),
    ('D', 'Drink'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

BREAK_CHOICES =(
    ('T', 'Morning Tea'),
    ('L', 'Lunch')
)

PAYMENT_CHOICES = (
    ('B', 'Pay with Card (Credit/Debit)') ,
    ('C', 'Pay with Cash at Tuck Shop')
)

# ADDRESS_CHOICES = (
#     ('B', 'Billing'),
#     ('S', 'Shipping'),
# )


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    discount_price = models.DecimalField(decimal_places=2,blank=True, null=True, max_digits=4)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField(default='', editable=False)
    description = models.TextField(blank = True, null = True)
    image = models.ImageField(upload_to='images/', default='static/img/no-image-available-icon-template-260nw-1036735678.jpg.png')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def save(self , *args , **kwargs):
        value = self.title
        self.slug = slugify(value , allow_unicode=True)
        super().save(*args , **kwargs)

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    pickup_date = models.DateField("Date" , default=datetime.date.today)
    break_choice = models.CharField(choices=BREAK_CHOICES, default='T', max_length=20)
    payment_option = models.CharField(max_length=20, choices= PAYMENT_CHOICES, default='B')
    order_total = models.DecimalField(decimal_places=2 , max_digits=4, default = 0.00)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    '''
    1. Item added to cart
    2. Add pickup date
    3. add pickup time
    '''
    # def order_window(self):
    #     if datetime.time < 9:
    #         self.current_window = datetime.date.today
    #     elif datetime.time > 9:
    #         self.current_window = datetime.date.today + 1


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total



class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
