import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from store.models import Category, Product, SubCategory


def create_slug(model, instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = model.objects.filter(slug=slug).order_by('pk')
    exists = qs.exists()
    if exists:
        uuid_start = str(uuid.uuid1()).split("-", 1)[0]
        new_slug = "%s-%s" % (slug, uuid_start)
        return create_slug(model, instance, new_slug=new_slug)

    return slug


@receiver(pre_save, sender=Category)
def pre_save_category_slug_reciever(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Category, instance)
    else:
        try:
            category = Category.objects.get(pk=instance.pk)
        except Category.DoesNotExist:
            pass
        if instance.name != category.name:
            instance.slug = create_slug(Category, instance)


@receiver(pre_save, sender=SubCategory)
def pre_save_sub_category_slug_reciever(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(SubCategory, instance)
    else:
        try:
            category = SubCategory.objects.get(pk=instance.pk)
        except SubCategory.DoesNotExist:
            pass
        if instance.name != category.name:
            instance.slug = create_slug(SubCategory, instance)


@receiver(pre_save, sender=Product)
def pre_save_product_slug_reciever(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Product, instance)
    else:
        try:
            product = Product.objects.get(pk=instance.pk)
        except Product.DoesNotExist:
            pass
        if instance.name != product.name:
            instance.slug = create_slug(Product, instance)
