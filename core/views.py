from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.shortcuts import redirect
from django.db.models import Q
from .forms import CheckoutForm, create_option_form
from copy import deepcopy

from .models import *
from .render import Render
import datetime


import random
import string


def create_ref_code():
    code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return code


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def home_redirect(request): # redirect for empty path to 'all' path
    response = redirect("core:all")
    return response


class CheckoutView(View):
    def get(self, *args, **kwargs):

        # Checks if Tuck shop is currently open and sets current order to the appropriate day
        time = CutoffTime.objects.get()
        cuttime = time.cutoff
        now = datetime.datetime.now().time()
        today = datetime.date.today()
        if now > cuttime:
            today = today + datetime.timedelta(days=1)

        status_open = True
        if today.weekday() in (5 , 6):
            status_open = False
        else:
            try:
                check = ClosedDate.objects.filter(closed_dates=today)
                if check.exists():
                    status_open = False
            except ObjectDoesNotExist:
                status_open = True
                
        if not status_open:
            return redirect("core:order-summary")
        else:
            try:
                today = today.strftime("%A %d/%m")
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.set_window()
                user = UserProfile.objects.get(user=self.request.user)
                form = CheckoutForm()
                context = {
                    'form': form,
                    # 'couponform': CouponForm(),
                    'order': order,
                    'user': user,
                    'date':today,
                    # 'DISPLAY_COUPON_FORM': True
                }

                return render(self.request, "checkout.html", context)
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:order-summary")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            if form.is_valid():
                order = Order.objects.get(user=self.request.user , ordered=False)
                order.get_total()

                order_items = order.items.all()
                order_items.update(ordered=True)

                order.break_choice = form.cleaned_data.get('break_choice')
                order.order_date = datetime.datetime.now()
                order.set_window()
                order.payment_option = form.cleaned_data.get('payment_option')

                order.ordered = True
                order.ref_code = create_ref_code()

                net_order, created = NetOrders.objects.get_or_create(
                    date=order.pickup_date
                )
                for order_item in order.items.all():
                    net_item, created= NetItem.objects.get_or_create(
                        date=net_order,
                        slug=order_item.slug,
                        title=order_item.title,
                    )
                    net_item.quantity += order_item.quantity
                    net_item.save()

                order.save()

                messages.success(self.request , "Your order was successful! View your orders in the 'Account & Orders' page")
                return redirect("/")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            # Checks if Tuck shop is currently open and sets current order to the appropriate day

            time = CutoffTime.objects.get()
            cuttime = time.cutoff
            now = datetime.datetime.now().time()
            today = datetime.date.today()
            day = "today"
            if now > cuttime:
                today = today + datetime.timedelta(days=1)
                day = "tomorrow"

            status_open = True
            if today.weekday() in (5 , 6): # closes tuck shop in weekend, disables ordering
                status_open = False
            else:
                try:
                    check = ClosedDate.objects.filter(closed_dates=today)
                    if check.exists():
                        status_open = False
                except ObjectDoesNotExist:
                    status_open = True

            today = today.strftime("%A %d/%m")

            context = {
                'object': order,
                'status': status_open,
                'date': today,
            }

            if not status_open:
                messages.warning(self.request , 'The Tuck Shop is currently closed. You can still add items to your cart to order when we reopen.')
            else:
                messages.info(self.request, 'Order for ' + day + ": " + str(today))

            return render(self.request, 'order_summary.html', context)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class AccountView(View):
    def get(self, request, *args, **kwargs):
        try:
            orders = Order.objects.filter(user=self.request.user, ordered=True).order_by('-order_date')
            profile = UserProfile.objects.get(user=self.request.user)
            context = {
                "orders": orders,
                "user": profile,

            }
            return render(self.request, "account.html", context)
        except TypeError:
            messages.info(self.request, "You are not currently signed in")
            return redirect("core:home")


# Ajax request to update modal
def update_variations(request):
    slug = request.GET.get('slug')
    item = Item.objects.get(slug=slug)
    variations_list = item.itemvariation_set.all() # returns all foreignkey relations for an item (backwards direction)
    context = {
        'item': item,
        'variations_list': variations_list,
    }
    return render(request, 'snippets/option_modal.html', context)


# ------------------------------------------------- Category and searching views ---------------------------------------

'''
Search bar
'''
def search(request):
    query = request.GET.get('q', '')
    if query:
        queryset = (Q(text__icontains=query))
        results = Item.objects.filter(queryset).distinct()
    else:
        results = []
    return render(request, 'home.html', {'results': results, 'query': query})


class SearchView(TemplateView):
    model = Item

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        self.object_list = Item.objects.filter(title__icontains=q)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(object_list=self.object_list, **kwargs)

    paginate_by = 12
    template_name = 'home.html'


class HomeView(ListView):
    model = Item
    paginate_by = 12
    template_name = "home.html"


class HotFoodView(ListView):
    model = Item

    def get_queryset(self):
        queryset = Item.objects.filter(category='HF')
        print(queryset)
        return queryset

    paginate_by = 12
    template_name = "home.html"


class ColdFoodView(ListView):
    model = Item

    def get_queryset(self):
        queryset = Item.objects.filter(category='CF')
        print(queryset)
        return queryset

    paginate_by = 12
    template_name = "home.html"


class SnacksView(ListView):
    model = Item

    def get_queryset(self):
        queryset = Item.objects.filter(category='S')
        print(queryset)
        return queryset

    paginate_by = 12
    template_name = "home.html"


class FrozenView(ListView):
    model = Item

    def get_queryset(self):
        queryset = Item.objects.filter(category='F')
        print(queryset)
        return queryset

    paginate_by = 12
    template_name = "home.html"


class DrinksView(ListView):
    model = Item

    def get_queryset(self):
        queryset = Item.objects.filter(category='D')
        print(queryset)
        return queryset

    paginate_by = 12
    template_name = "home.html"

#-----------------------------------------------------------------------------------------------------------------------





class ItemDetailView(DetailView):
    model = Item
    template_name = "item.html"


def add_order_to_cart(request, ref_code):
    past_order = get_object_or_404(Order, ref_code=ref_code)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order_qs.delete()

    for orderitem in OrderItem.objects.filter(user=request.user, ordered=False):
        orderitem.delete()

    order_date = timezone.now()
    order = Order.objects.create(
        user=request.user,
        order_date=order_date,
        break_choice=past_order.break_choice
    )

    for element in past_order.items.all():
        #error checking statements to check if the item is marked as avaliable or still exists, item must be available (must be pure item and not variation or must be variation and available)
        if not element.item.not_available and ((element.item and not element.item_variations) or (element.item_variations and not element.item_variations.not_available and not element.item_variations.item.not_available)):
            element.pk = None
            order_item = element
            order_item.ordered = False
            order_item.save()
            order.items.add(order_item)
        else:
            messages.info(request , "One or more items in your previous order are longer available.")


    messages.info(request , "This order was added to your cart.")
    return redirect("core:order-summary")


@login_required
def add_to_cart(request, slug):
    try:
        variation_item = ItemVariation.objects.get(slug=slug)
        item = variation_item.item
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            item_variations=variation_item,
            slug=slug,
            ordered=False
        )

    except ObjectDoesNotExist:
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            slug=slug,
            ordered=False
        )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(slug=slug).exists(): # problematic statement as there are seperate slugs for variations and items
            if order_item.quantity < order_item.item.maximum_quantity:
                order_item.quantity += 1
                order_item.save()
                messages.info(request , "This item quantity was updated.")
                return redirect("core:order-summary")
            else:
                messages.info(request , "Maximum Quantity Reached")
                return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request , "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        order_date = timezone.now()
        order = Order.objects.create(
            user=request.user , order_date=order_date)
        order.items.add(order_item)
        messages.info(request , "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(slug=slug).exists():
            order_item = OrderItem.objects.filter(
                slug=slug,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:order-summary", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(slug=slug).exists():
            order_item = OrderItem.objects.filter(
                slug=slug,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request , "This item quantity was updated.")
                return redirect("core:order-summary")
            else:
                order.items.remove(order_item)
                messages.info(request , "This item was removed from your cart.")
                return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


# def get_coupon(request, code):
#     try:
#         coupon = Coupon.objects.get(code=code)
#         return coupon
#     except ObjectDoesNotExist:
#         messages.info(request, "This coupon does not exist")
#         return redirect("core:checkout")
#
#
# class AddCouponView(View):
#     def post(self, *args, **kwargs):
#         form = CouponForm(self.request.POST or None)
#         if form.is_valid():
#             try:
#                 code = form.cleaned_data.get('code')
#                 order = Order.objects.get(
#                     user=self.request.user, ordered=False)
#                 order.coupon = get_coupon(self.request, code)
#                 order.save()
#                 messages.success(self.request, "Successfully added coupon")
#                 return redirect("core:checkout")
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "You do not have an active order")
#                 return redirect("core:checkout")


'''

Printout Views for admin page

'''


class MorningOrderPrintout(View):
    def get(self, *args, **kwargs):

        pickup_date = datetime.date.today()
        queryset = Order.objects.filter(pickup_date=pickup_date,
                                        break_choice='T',
                                        ordered="True"
                                        ).order_by('user')

        params = {
            'queryset': queryset,
            'today': pickup_date,
            'break': "Morning Tea",
        }
        return Render.render('admin/order_printout.html', params)


class LunchOrderPrintout(View):
    def get(self, *args, **kwargs):

        pickup_date = datetime.date.today()
        queryset = Order.objects.filter(pickup_date=pickup_date,
                                        break_choice='L',
                                        ordered='True'
                                        ).order_by('user')
        params = {
            'queryset': queryset,
            'today': pickup_date,
            'break': "Lunch",
        }
        return Render.render('admin/order_printout.html', params)


class NetOrderPrintout(View):
    def get(self, *args, **kwargs):
        try:
            pickup_date = datetime.date.today()
            queryset = NetOrders.objects.get(date=pickup_date)
            params = {
                'queryset': queryset,
                'today': pickup_date,
            }
            return Render.render('admin/net_order_printout.html', params)
        except ObjectDoesNotExist:
            return redirect('/admin')

