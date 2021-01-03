from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from filer.models import ThumbnailOption
from shop.admin.defaults import customer
from shop.admin.defaults.order import OrderAdmin
from shop.models.defaults.order import Order
from shop.admin.delivery import DeliveryOrderAdminMixin
from adminsortable2.admin import SortableAdminMixin
from shop.admin.product import CMSPageAsCategoryMixin, UnitPriceMixin, ProductImageInline, InvalidateProductCacheMixin, SearchProductIndexMixin
from myshop.models import Manufacturer, SmartCard


admin.site.site_header = "My SHOP Administration"
admin.site.unregister(ThumbnailOption)


@admin.register(Order)
class OrderAdmin(DeliveryOrderAdminMixin, OrderAdmin):
    pass


admin.site.register(Manufacturer, admin.ModelAdmin)

__all__ = ['customer']


@admin.register(SmartCard)
class SmartCardAdmin(InvalidateProductCacheMixin, SearchProductIndexMixin, SortableAdminMixin, CMSPageAsCategoryMixin, UnitPriceMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                ('product_name', 'slug'),
                ('product_code', 'unit_price'),
                'quantity',
                'active',
                'caption',
                'description',
            ],
        }),
        (_("Properties"), {
            'fields': ['manufacturer', 'storage', 'card_type'],
        }),
    ]
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ['product_name']}
    list_display = ['product_name', 'product_code', 'get_unit_price', 'active']
    search_fields = ['product_name']
