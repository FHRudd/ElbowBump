from django.contrib import admin
from .models import *


# Register your models here.
class ProductVariantInline(admin.TabularInline):
    model = Variation


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Variation)
admin.site.register(GalleryImages)


