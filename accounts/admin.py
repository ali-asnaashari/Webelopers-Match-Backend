from django.contrib import admin

from accounts.models import Product, ShoppingCard


class ProductAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ('name', 'price', 'quantity')

class ShoppingCardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCard, ShoppingCardAdmin)
