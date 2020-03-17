from django.contrib import admin
from .models import products,Account,ShippingDetail,Cart,NewTable
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','sku','slug','image','pub_date','page','qty','imagelink')

class CartAdmin(admin.ModelAdmin):
    list_display = ('productName','price','BuyerName','qty','email','order_date','productsku')

 

admin.site.register(products, ProductAdmin)
admin.site.register(Account)
admin.site.register(ShippingDetail)
admin.site.register(Cart, CartAdmin)
admin.site.register(NewTable)

