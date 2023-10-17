import auto_prefetch
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

from sinum.utils.media import MediaHelper
from sinum.utils.models import (CategoryModel, NamedTimeBasedModel,
                                TimeBasedModel)
from store.fields import OrderField


class Category(CategoryModel):
    sub_categories = models.ManyToManyField(
        "store.SubCategory",
        blank=True,
        related_name="category"
    )

    def __str__(self):
        return self.name

    @property
    def subcategories(self):
        return self.sub_categories.all()


class SubCategory(CategoryModel):

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["name", "created_at"]
        indexes = [
            models.Index(fields=("name",)),
            models.Index(fields=("created_at",), )
        ]
        verbose_name_plural = 'sub categories'

    def __str__(self):
        return f"{self.name}"


class Product(NamedTimeBasedModel):
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    vendor_store = auto_prefetch.ForeignKey(
        "vendor.VendorStore",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="products"
    )
    category = auto_prefetch.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    sub_categories = models.ManyToManyField(
        SubCategory,
        blank=True,
        related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = RichTextField(blank=True)
    image = models.ImageField(
        help_text="Product Featured Image",
        blank=True,
        upload_to=MediaHelper.get_image_upload_path
    )
    in_stock = models.BooleanField(default=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    specification = RichTextField(blank=True)

    class Meta(auto_prefetch.Model.Meta):
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"http://localhost:8000/{settings.STATIC_URL}avatars/placeholder.jpg"

    def __str__(self):
        return self.name


class ProductImage(TimeBasedModel):
    text = models.CharField(max_length=50, blank=True)
    product = auto_prefetch.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="product_images",
        null=True,
    )
    image = models.ImageField(
        blank=True,
        upload_to=MediaHelper.get_image_upload_path
    )
    order = OrderField(
        blank=True,
        for_fields=['product'],
        help_text='Image order number'
    )

    def __str__(self):
        return f"{self.product.name} images"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"http://localhost:8000/{settings.STATIC_URL}avatars/placeholder.jpg"
