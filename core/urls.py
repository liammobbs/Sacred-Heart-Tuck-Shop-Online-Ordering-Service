from django.urls import path
from .views import (
    home_redirect,
    ItemDetailView,
    CheckoutView,
    HomeView,
    HotFoodView,
    ColdFoodView,
    SnacksView,
    FrozenView,
    DrinksView,
    OrderSummaryView,
    add_to_cart,
    add_order_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    # PaymentView,
    AddCouponView,
    MorningOrderPrintout,
    LunchOrderPrintout,
    NetOrderPrintout,
    AccountView,
    SearchView,
    TopupView,
    CheckoutTopupView,
    # RequestRefundView
)

app_name = 'core'

urlpatterns = [
    path('', home_redirect, name='home'),
    path('all', HomeView.as_view(), name='all'),
    path('hot-food', HotFoodView.as_view(), name='hot-food'),
    path('cold-food', ColdFoodView.as_view(), name='cold-food'),
    path('snacks', SnacksView.as_view(), name='snacks'),
    path('frozen', FrozenView.as_view(), name='frozen'),
    path('drinks', DrinksView.as_view(), name='drinks'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

    path('account/', AccountView.as_view(), name='account'),
    path('account/topup',TopupView.as_view(), name ='topup'),

    path('checkout/topup',CheckoutTopupView.as_view(), name= 'checkout-topup'),

    path(r'^search/$/', SearchView.as_view(), name='search'),

    path('render/morning-orders', MorningOrderPrintout.as_view(), name='morning-orders-printout'),
    path('render/lunch-orders', LunchOrderPrintout.as_view(), name='lunch-orders-printout'),
    path('render/net-orders',NetOrderPrintout.as_view(), name= 'net-orders-printout'),

    path('product/<slug>/', ItemDetailView.as_view() , name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-order-to-cart/<ref_code>/', add_order_to_cart, name='add-order-to-cart'),

    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart')
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
