
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from shop.money.fields import MoneyField
from shop.models.product import BaseProduct, BaseProductManager, AvailableProductMixin, CMSPageReferenceMixin
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.order import BaseOrderItem
from shop.models.defaults.delivery import Delivery
from shop.models.defaults.delivery_item import DeliveryItem
from shop.models.defaults.order import Order
from shop.models.defaults.mapping import ProductPage, ProductImage
from shop.models.defaults.address import BillingAddress, ShippingAddress
from shop.models.defaults.customer import Customer


__all__ = ['Cart', 'CartItem', 'Order', 'Delivery', 'DeliveryItem',
           'BillingAddress', 'ShippingAddress', 'Customer', ]


class OrderItem(BaseOrderItem):
    quantity = models.PositiveIntegerField(_("Ordered quantity"))
    canceled = models.BooleanField(_("Item canceled "), default=False)


class Manufacturer(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class ProductManager(BaseProductManager):
    pass


class SmartCard(CMSPageReferenceMixin, AvailableProductMixin, BaseProduct):
    product_name = models.CharField(
        max_length=255,
        verbose_name=_("Product Name"),
    )

    slug = models.SlugField(verbose_name=_("Slug"))

    caption = HTMLField(
        _("Caption"),
        configuration='CKEDITOR_SETTINGS_CAPTION',
        help_text=_("Short description used in the catalog's list view."),
    )

    # product properties
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name=_("Manufacturer"),
    )

    # controlling the catalog
    order = models.PositiveIntegerField(
        _("Sort by"),
        db_index=True,
    )

    cms_pages = models.ManyToManyField(
        'cms.Page',
        through=ProductPage,
        help_text=_("Choose list view this product shall appear on."),
    )

    images = models.ManyToManyField(
        'filer.Image',
        through=ProductImage,
    )

    unit_price = MoneyField(
        _("Unit price"),
        decimal_places=3,
        help_text=_("Net price for this product"),
    )

    card_type = models.CharField(
        _("Card Type"),
        choices=[2 * ('{}{}'.format(s, t),)
                 for t in ['SD', 'SDXC', 'SDHC', 'SDHC II'] for s in ['', 'micro ']],
        max_length=15,
    )

    speed = models.CharField(
        _("Transfer Speed"),
        choices=[(str(s), "{} MB/s".format(s))
                 for s in [4, 20, 30, 40, 48, 80, 95, 280]],
        max_length=8,
    )

    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )

    storage = models.PositiveIntegerField(
        _("Storage Capacity"),
        help_text=_("Storage capacity in GB"),
    )

    description = HTMLField(
        _("Description"),
        configuration='CKEDITOR_SETTINGS_DESCRIPTION',
        help_text=_("Long description for the detail view of this product."),
    )

    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock")
    )

    class Meta:
        verbose_name = _("Smart Card")
        verbose_name_plural = _("Smart Cards")
        ordering = ['order']

    # filter expression used to lookup for a product item using the Select2 widget
    lookup_fields = ['product_code__startswith', 'product_name__icontains']

    def get_price(self, request):
        return self.unit_price

    objects = ProductManager()

    def __str__(self):
        return self.product_name

    @property
    def sample_image(self):
        return self.images.first()
