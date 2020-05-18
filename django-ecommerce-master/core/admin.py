from django.contrib import admin

from .models import Item, OrderItem, Order, UserProfile


# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)
#
#
# make_refund_accepted.short_description = 'Update orders to refund granted'
class ItemAdmin(admin.ModelAdmin):
    list_display=['title',
                  'price',
                  'category']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'pickup_date',
                    'break_choice',
                    'payment_option',
                    'ordered',
                    ]

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment)
# admin.site.register(Coupon)
# admin.site.register(Refund)
# admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
