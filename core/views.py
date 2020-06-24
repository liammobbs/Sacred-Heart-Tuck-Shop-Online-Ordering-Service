from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.shortcuts import redirect
from django.db.models import Q
from .forms import CheckoutForm
# ,CouponForm

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


def home_redirect(request):
    response = redirect("core:all")
    return response


class CheckoutView(View):
    def get(self, *args, **kwargs):
        time = CutoffTime.objects.get()
        cuttime = time.cutoff
        now = datetime.datetime.now().time()
        today = datetime.date.today()
        status_open = True
        if now > cuttime or today.weekday() in (5, 6):
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
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.set_window()
                user = UserProfile.objects.get(user = self.request.user)
                form = CheckoutForm()
                context = {
                    'form': form,
                    # 'couponform': CouponForm(),
                    'order': order,
                    'user': user,
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
                    try:
                        item = order_item.item
                        quantity = order_item.quantity
                        net_order_item = NetOrders.objects.get(net_item__item=item , date=order.pickup_date)
                        for element in net_order_item.net_item.all():
                            if element.item == item:
                                element.quantity += quantity
                                element.save()

                    except ObjectDoesNotExist:
                        net_order.net_item.add(order_item)

                net_order.save()

                order.save()

                messages.success(self.request , "Your order was successful!")
                return redirect("/")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class AccountView(View):
    def get (self, request, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user, ordered=True).order_by('-order_date')
        profile = UserProfile.objects.get(user=self.request.user)
        context = {
            "orders": orders,
            "user": profile,

        }
        return render(self.request, "account.html", context)


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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            time = CutoffTime.objects.get()
            cuttime = time.cutoff
            now = datetime.datetime.now().time()
            today = datetime.date.today()

            status_open = True
            if now > cuttime or today.weekday() in (5 , 6):
                status_open = False
            else:
                try:
                    check = ClosedDate.objects.filter(closed_dates=today)
                    if check.exists():
                        status_open = False
                except ObjectDoesNotExist:
                    status_open = True

            context = {
                'object': order,
                'status': status_open,
            }

            if not status_open:
                messages.warning(self.request , 'The Tuck Shop is currently closed. You can still add items to your cart to order when we reopen.')

            return render(self.request, 'order_summary.html', context)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_order_to_cart(request, ref_code):
    past_order = get_object_or_404(Order, ref_code=ref_code)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order_qs.delete()

    order_date = timezone.now()
    order = Order.objects.create(
        user=request.user,
        order_date=order_date,
        break_choice=past_order.break_choice
    )

    for element in past_order.items.all():
        item = element.item
        quantity=element.quantity
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            quantity=quantity,
            user=request.user,
            ordered=False
        )
        order.items.add(order_item)

    messages.info(request , "This order was added to your cart.")
    return redirect("core:order-summary")


@login_required
def add_to_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity < order_item.item.maximum_quantity:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("core:order-summary")
            else:
                messages.info(request, "Maximum Quantity Reached")
                return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        order_date = timezone.now()
        order = Order.objects.create(
            user=request.user, order_date=order_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    try:
        item = ItemVariation.objects.get(slug=slug)
    except ObjectDoesNotExist:
        item = get_object_or_404(Item , slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
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
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
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
                                        ordered ="True"
                                        )

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
                                        )

        params = {
            'queryset': queryset,
            'today': pickup_date,
            'break': "Lunch",
        }
        return Render.render('admin/order_printout.html', params)


class NetOrderPrintout(View):
    def get(self, *args, **kwargs):
        pickup_date = datetime.date.today()
        queryset = NetOrders.objects.filter(date=pickup_date)
        params = {
            'queryset': queryset,
            'today': pickup_date,
        }
        return Render.render('admin/net_order_printout.html', params)


