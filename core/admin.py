from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import *
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test

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


def require_confirmation(func):
    def wrapper(request, queryset):
        if request.POST.get("confirmation") is None:
            request.current_app = modeladmin.admin_site.name
            context = {
                "action": request.POST["action"],
                "queryset":queryset
            }
            return TemplateResponse(request, "admin/action_confirmation.html", context)

        return func(request)

    wrapper.__name__ = func.__name__
    return wrapper



@staff_member_required
@user_passes_test(lambda u: u.is_superuser)
def clear_user_data(request):

    messages.add_message(request , messages.INFO , "(TEST MESSAGE) All User Data has been cleared")
    # for obj in User.objects.filter(is_staff=False, is_superuser=False):
    #     obj.delete()

    return redirect('/admin')


class RefundInlineAdmin(admin.TabularInline):
    model = Refund
    fields = ['reason' ,
              'accepted',
              ]


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
                    'user_link',
                    'pickup_date' ,
                    'break_choice' ,
                    'payment_option' ,
                    'order_total' ,
                    'ordered' ,

                    ]

    list_display_links = ['ref_code',
                    'user_link',]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)),
            obj.user
        ))

    user_link.short_description = 'user'

    list_filter = ['pickup_date' , ]
    search_fields = ['ref_code' , 'user__username']

    # actions = [make_refund_accepted]
    # inlines = [RefundInlineAdmin]


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

class OrderInlineAdmin(admin.TabularInline):
    model = Order
    show_change_link = True
    extra = 0
    fields = [
        'ref_code',
        'pickup_date',
        'break_choice',
        'order_total',
    ]

    readonly_fields = [
        'ref_code',
        'pickup_date',
        'break_choice',
        'order_total',
    ]

    ordering = ("-pickup_date",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request , obj=None):
        return False



class UserProfileInlineAdmin(admin.TabularInline):
    model = UserProfile
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



class UserAdmin(UserAdmin):
    change_list_template = "admin/user_profile_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('clear_user_data/', clear_user_data),
        ]
        return my_urls + urls
    inlines = (UserProfileInlineAdmin, OrderInlineAdmin,)



admin.site.site_header = "Sacred Heart Tuck Shop Admin"



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Item , ItemAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order , OrderAdmin)
# admin.site.register(Payment)
# admin.site.register(Coupon)
# admin.site.register(Refund)
# admin.site.register(UserProfile , UserProfileAdmin)
admin.site.register(NetOrders , NetOrdersAdmin)
# admin.site.register(NetItem)
admin.site.register(CutoffTime , CutoffAdmin)
admin.site.register(ClosedDate , ClosedDateAdmin)

