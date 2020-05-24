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
    list_filter = ['category']

class OrderAdmin(admin.ModelAdmin):
    fields = ['user',
              'ref_code',
              'pickup_date' ,
              'break_choice' ,
              'items',
              'order_total' ,
              'payment_option' ,
              'ordered' ,
              ]
    readonly_fields = ['user',
              'ref_code',
              'pickup_date' ,
              'break_choice' ,
              'payment_option' ,
              'items',
              'order_total' ,
              'ordered' ,]

    list_display = ['user',
                    'pickup_date',
                    'break_choice',
                    'payment_option',
                    'order_total',
                    'ordered',

                    ]
    list_filter = ['pickup_date',]

class OrderItemAdmin(admin.ModelAdmin):
    fields = ['user' ,
              'item' ,
              'quantity',
              'ordered' ,
              ]

    readonly_fields = ['user' ,
                      'item' ,
                      'quantity',
                      'ordered' ,
                       ]
    list_display = ['user',
                    'item',
                    'quantity',
                    'ordered',
    ]

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment)
# admin.site.register(Coupon)
# admin.site.register(Refund)
# admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
