from django.contrib import admin

from .models import *


# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)
#
#
# make_refund_accepted.short_description = 'Update orders to refund granted'



class OrderAdmin(admin.ModelAdmin):
    fields = ['user' ,
              'ref_code' ,
              'pickup_date' ,
              'break_choice' ,
              'items' ,
              'order_total' ,
              'payment_option' ,
              'ordered' ,
              ]


    def get_readonly_fields(self , request , obj=None):
        if obj:
            return ['user' ,
                       'ref_code' ,
                       'break_choice' ,
                       'payment_option' ,
                       'items' ,
                       'order_total' ,
                       ]
        else:
            return ['order_total']

    list_display = ['user' ,
                    'pickup_date' ,
                    'break_choice' ,
                    'payment_option' ,
                    'order_total' ,
                    'ordered' ,

                    ]
    list_filter = ['pickup_date' , ]
    search_fields = ['ref_code' , 'user__username']


class OrderItemAdmin(admin.ModelAdmin):
    fields = ['user' ,
              'title',
              'quantity' ,
              'ordered' ,
              ]

    readonly_fields = ['user' ,
                       'title',
                       'quantity' ,
                       'ordered' ,
                       ]
    list_display = ['user' ,
                    'title' ,
                    'quantity' ,
                    'ordered' ,
                    ]


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user' ,
              'firstname' ,
              'lastname' ,
              'user_email'
              ]

    readonly_fields = ['user' ,
                       'firstname' ,
                       'lastname' ,
                       'user_email'
                       ]
    list_display = ['user' ,
                    'firstname' ,
                    'lastname' ,
                    'user_email'
                    ]


class NetOrdersAdmin(admin.ModelAdmin):
    fields = ['date' ,
              'net_item']

    readonly_fields = [
        'date' ,
        'net_item'
    ]

    list_display = ['date']

    def has_add_permission(self , request , obj=None):
        return False


class CutoffAdmin(admin.ModelAdmin):
    list_display = ["cutoff"]

    def has_add_permission(self , request , obj=None):
        return False


class ClosedDateAdmin(admin.ModelAdmin):
    list_display = ['closed_dates']


class ItemVariationInLineAdmin(admin.TabularInline):
    model = ItemVariation
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title' ,
                    'category',
                    'price' ,
                    'discount_price' ,
                    ]
    list_filter = ['category', 'not_available', 'variations_exist']
    search_fields = ['title']

    inlines = [ItemVariationInLineAdmin]





admin.site.site_header = "Sacred Heart Tuck Shop Admin"
admin.site.register(Item , ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order , OrderAdmin)
# admin.site.register(Payment)
# admin.site.register(Coupon)
# admin.site.register(Refund)
admin.site.register(UserProfile , UserProfileAdmin)
admin.site.register(NetOrders , NetOrdersAdmin)
admin.site.register(CutoffTime , CutoffAdmin)
admin.site.register(ClosedDate , ClosedDateAdmin)