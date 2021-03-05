from django.contrib import admin

from accounts.models import Product


class ProductAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ('name', 'price', 'quantity')


admin.site.register(Product, ProductAdmin)
