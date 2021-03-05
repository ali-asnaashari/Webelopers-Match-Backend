from django.contrib.auth.views import LoginView
from django.urls import path

from accounts.views import signup, logout_user, panel, create_item, AllProducts, edit, delete_product, \
    EntireProducts, product_page, rate, order, cart, cart_delete

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('panel/', panel, name='panel'),
    path('create_item/', create_item, name='create_item'),
    path('cart/<id>/', cart, name='cart'),
    path('cart/delete/<pk>/',cart_delete, name='cart_delete'),
    path('rate/<id>/<redirect_page>', rate, name='rate'),
    path("order/", order, name='order'),
    path('all_products/', AllProducts.as_view(), name='all_products'),
    path('entire_products/', EntireProducts.as_view(), name='entire_products'),
    path('edit/<id>/', edit, name='edit'),
    path('product/<id>/', product_page, name='product_page'),
    path('delete_product/<id>/', delete_product, name='delete_product'),

]
