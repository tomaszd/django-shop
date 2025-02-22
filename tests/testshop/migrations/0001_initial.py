# Generated by Django 3.0.11 on 2021-01-03 15:03

import cms.models.fields
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc
import django_fsm
import djangocms_text_ckeditor.fields
import filer.fields.image
import shop.models.address
import shop.models.defaults.commodity
import shop.models.fields
import shop.models.inventory
import shop.models.product
import shop.money.fields
import shop.payment.workflows
import shop.shipping.workflows


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('email_auth', '0005_auto_20191123_2051'),
        ('cms', '0022_auto_20180620_1551'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.SmallIntegerField(db_index=True, default=0, help_text='Priority for using this address')),
                ('name', models.CharField(max_length=1024, verbose_name='Full name')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('country', shop.models.address.CountryField(verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Billing Address',
                'verbose_name_plural': 'Billing Addresses',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('extra', shop.models.fields.JSONField(verbose_name='Arbitrary information for this cart')),
                ('billing_address', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to='testshop.BillingAddress')),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('active', models.BooleanField(default=True, help_text='Is this product publicly visible.', verbose_name='Active')),
                ('product_name', models.CharField(max_length=255, verbose_name='Product Name')),
                ('product_code', models.CharField(max_length=255, unique=True, verbose_name='Product code')),
                ('unit_price', shop.money.fields.MoneyField(decimal_places=3, help_text='Net price for this product', verbose_name='Unit price')),
                ('order', models.PositiveIntegerField(db_index=True, verbose_name='Sort by')),
                ('show_breadcrumb', models.BooleanField(default=True, help_text="Shall the detail page show the product's breadcrumb.", verbose_name='Show Breadcrumb')),
                ('quantity', models.PositiveIntegerField(default=0, help_text='Available quantity in stock', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('caption', djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Short description for the catalog list view.', null=True, verbose_name='Caption')),
            ],
            options={
                'verbose_name': 'Commodity',
                'verbose_name_plural': 'Commodities',
                'ordering': ('order',),
            },
            bases=(shop.models.product.CMSPageReferenceMixin, shop.models.defaults.commodity.CommodityMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='customer', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('recognized', shop.models.fields.ChoiceEnumField(help_text='Designates the state the customer is recognized as.', verbose_name='Recognized as')),
                ('last_access', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last accessed')),
                ('extra', shop.models.fields.JSONField(editable=False, verbose_name='Extra information about this customer')),
                ('number', models.PositiveIntegerField(default=None, null=True, unique=True, verbose_name='Customer Number')),
                ('salutation', models.CharField(choices=[('mrs', 'Mrs.'), ('mr', 'Mr.'), ('na', '(n/a)')], max_length=5, verbose_name='Salutation')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_id', models.CharField(blank=True, help_text="The transaction processor's reference", max_length=255, null=True, verbose_name='Shipping ID')),
                ('fulfilled_at', models.DateTimeField(blank=True, help_text='Timestamp of delivery fulfillment', null=True, verbose_name='Fulfilled at')),
                ('shipped_at', models.DateTimeField(blank=True, help_text='Timestamp of delivery shipment', null=True, verbose_name='Shipped at')),
                ('shipping_method', models.CharField(help_text='The shipping backend used to deliver items of this order', max_length=50, verbose_name='Shipping method')),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
                'get_latest_by': 'shipped_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_fsm.FSMField(default='new', max_length=50, protected=True, verbose_name='Status')),
                ('currency', models.CharField(editable=False, help_text='Currency in which this order was concluded', max_length=7)),
                ('_subtotal', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Subtotal')),
                ('_total', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Total')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('extra', shop.models.fields.JSONField(help_text='Arbitrary information for this order object on the moment of purchase.', verbose_name='Extra fields')),
                ('stored_request', shop.models.fields.JSONField(help_text='Parts of the Request objects on the moment of purchase.')),
                ('number', models.PositiveIntegerField(default=None, null=True, unique=True, verbose_name='Order Number')),
                ('shipping_address_text', models.TextField(blank=True, help_text='Shipping address at the moment of purchase.', null=True, verbose_name='Shipping Address')),
                ('billing_address_text', models.TextField(blank=True, help_text='Billing address at the moment of purchase.', null=True, verbose_name='Billing Address')),
                ('token', models.CharField(editable=False, help_text='Secret key to verify ownership on detail view without requiring authentication.', max_length=40, null=True, verbose_name='Token')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='testshop.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=(shop.payment.workflows.ManualPaymentWorkflowMixin, shop.payment.workflows.CancelOrderWorkflowMixin, shop.shipping.workflows.PartialDeliveryWorkflowMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MyProduct',
            fields=[
                ('commodity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='testshop.Commodity')),
            ],
            bases=(shop.models.inventory.AvailableProductMixin, 'testshop.commodity'),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.SmallIntegerField(db_index=True, default=0, help_text='Priority for using this address')),
                ('name', models.CharField(max_length=1024, verbose_name='Full name')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('country', shop.models.address.CountryField(verbose_name='Country')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Customer')),
            ],
            options={
                'verbose_name': 'Shipping Address',
                'verbose_name_plural': 'Shipping Addresses',
            },
        ),
        migrations.CreateModel(
            name='ProductPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Page')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Commodity')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'abstract': False,
                'unique_together': {('page', 'product')},
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(default=0)),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, to=settings.FILER_IMAGE_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Commodity')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', shop.money.fields.MoneyField(help_text='How much was paid with this particular transfer.', verbose_name='Amount paid')),
                ('transaction_id', models.CharField(help_text="The transaction processor's reference", max_length=255, verbose_name='Transaction ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Received at')),
                ('payment_method', models.CharField(help_text='The payment backend used to process the purchase', max_length=50, verbose_name='Payment method')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order payment',
                'verbose_name_plural': 'Order payments',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, help_text='Product name at the moment of purchase.', max_length=255, null=True, verbose_name='Product name')),
                ('product_code', models.CharField(blank=True, help_text='Product code at the moment of purchase.', max_length=255, null=True, verbose_name='Product code')),
                ('_unit_price', models.DecimalField(decimal_places=2, help_text='Products unit price at the moment of purchase.', max_digits=30, null=True, verbose_name='Unit price')),
                ('_line_total', models.DecimalField(decimal_places=2, help_text='Line total on the invoice at the moment of purchase.', max_digits=30, null=True, verbose_name='Line Total')),
                ('extra', shop.models.fields.JSONField(help_text='Arbitrary information for this order item', verbose_name='Extra fields')),
                ('quantity', models.PositiveIntegerField()),
                ('canceled', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='testshop.Order', verbose_name='Order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='testshop.Commodity', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Delivered quantity')),
                ('delivery', models.ForeignKey(help_text='Refer to the shipping provider used to ship this item', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='testshop.Delivery', verbose_name='Delivery')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliver_item', to='testshop.OrderItem', verbose_name='Ordered item')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Order'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='cms_pages',
            field=models.ManyToManyField(help_text='Choose list view this product shall appear on.', through='testshop.ProductPage', to='cms.Page'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='placeholder',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, slotname='Commodity Details', to='cms.Placeholder'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_testshop.commodity_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='sample_image',
            field=filer.fields.image.FilerImageField(blank=True, default=None, help_text="Sample image used in the catalog's list view.", null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.FILER_IMAGE_MODEL, verbose_name='Sample Image'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(blank=True, help_text='Product code of added item.', max_length=255, null=True, verbose_name='Product code')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('extra', shop.models.fields.JSONField(verbose_name='Arbitrary information for this cart item')),
                ('quantity', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='testshop.Cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Commodity')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='testshop.Customer', verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='shipping_address',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to='testshop.ShippingAddress'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testshop.Customer'),
        ),
        migrations.CreateModel(
            name='MyProductInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earliest', models.DateTimeField(db_index=True, default=datetime.datetime(1, 1, 1, 0, 0, tzinfo=utc), verbose_name='Available after')),
                ('latest', models.DateTimeField(db_index=True, default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc), verbose_name='Available before')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_set', to='testshop.MyProduct')),
            ],
            options={
                'verbose_name': 'Product Inventory',
                'verbose_name_plural': 'Product Inventories',
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='delivery',
            unique_together={('shipping_method', 'shipping_id')},
        ),
    ]
