from django.contrib import admin
from .models import products,Account,ShippingDetail,Cart,NewTable
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','slug','image','pub_date',)



admin.site.register(products, ProductAdmin)
admin.site.register(Account)
admin.site.register(ShippingDetail)
admin.site.register(Cart)
admin.site.register(NewTable)

