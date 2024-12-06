from django.contrib import admin
from .models import Customer, Product, Subscription

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'pan')
    search_fields = ('customer_id', 'name')
    list_filter = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'annual_cost')
    search_fields = ('product_name',)

class SubscriptionAdmin(admin.ModelAdmin):
    def get_subscription_id(self, obj):
        return str(obj.id)
    get_subscription_id.short_description = 'Subscription ID'

    list_display = ('get_subscription_id', 'customer', 'product', 'start_date', 'end_date', 'users')
    search_fields = ('customer__name', 'product__product_name')
    list_filter = ('start_date', 'end_date')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subscription, SubscriptionAdmin)