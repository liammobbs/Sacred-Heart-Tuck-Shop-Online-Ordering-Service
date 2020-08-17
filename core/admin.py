from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin
from .models import *


# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)
#
#
# make_refund_accepted.short_description = 'Update orders to refund granted'

def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(obj):
        linked_obj = getattr(obj , field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name , args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>' , link_url , linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


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

    list_display = ['ref_code',
                    'user',
                    'pickup_date' ,
                    'break_choice' ,
                    'payment_option' ,
                    'order_total' ,
                    'ordered' ,

                    ]
    list_filter = ['pickup_date' , ]
    search_fields = ['ref_code' , 'user__username']

#
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


class NetItemInLineAdmin(admin.TabularInline):
    model = NetItem
    extra = 0
    fields = ['title' ,
              'quantity' ,
              ]

    readonly_fields = [
                       'title' ,
                       'quantity',
    ]

    def has_add_permission(self , request):
        return False

    def has_delete_permission(self , request , obj=None):
        return False


class NetOrdersAdmin(admin.ModelAdmin):
    fields = ['date']

    readonly_fields = [
        'date',
    ]

    list_display = ['date']

    inlines = [NetItemInLineAdmin]

    def has_add_permission(self , request , obj=None):
        return False

    def has_delete_permission(self , request , obj=None):
        return False

    # def netorders_actions(self , obj):
    #     return format_html(
    #         '<a class="button" href="{}">Print Packing sheet</a>',
    #      
    #     )
    #
    # account_actions.short_description = 'Account Actions'
    # account_actions.allow_tags = True

class CutoffAdmin(admin.ModelAdmin):
    list_display = ["cutoff"]

    def has_add_permission(self , request , obj=None):
        return False


class ClosedDateAdmin(admin.ModelAdmin):
    list_display = ['closed_dates']




class ItemVariationInLineAdmin(admin.TabularInline):
    model = ItemVariation
    extra = 0

    exclude = ['slug']


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
# admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order , OrderAdmin)
# admin.site.register(Payment)
# admin.site.register(Coupon)
# admin.site.register(Refund)
admin.site.register(UserProfile , UserProfileAdmin)
admin.site.register(NetOrders , NetOrdersAdmin)
# admin.site.register(NetItem)
admin.site.register(CutoffTime , CutoffAdmin)
admin.site.register(ClosedDate , ClosedDateAdmin)