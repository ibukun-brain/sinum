from django.contrib import admin

from store.models import Category, Product, ProductImage, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    filter_horizontal = ['sub_categories']
    search_fields = ['name']
    list_filter = ['created_at', 'updated_at', 'visible']
    date_hierarchy = 'created_at'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    date_hierarchy = 'created_at'
    list_filter = ['created_at', 'updated_at', 'visible']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    # fields = ('text', 'image')
    # readonly_fields = ['vendor_store']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'vendor_store',
        'category',
        'price_in_naira',
        'in_stock',
        'quantity',
    ]
    search_fields = [
        'name',
        'vendor_store__name',
        'category__name',
    ]
    filter_horizontal = [
        'sub_categories'
    ]
    list_select_related = ['vendor_store', 'category']
    # autocomplete_fields = ['category', 'vendor_store']
    raw_id_fields = ['category', 'vendor_store']
    inlines = [ProductImageInline]
    date_hierarchy = 'created_at'
    list_filter = ['created_at', 'visible']
    list_per_page = 100

    def price_in_naira(self, obj):
        return f"₦{obj.price}"
    price_in_naira.short_description = "price (₦)"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['text', 'product']
    list_display_links = ['product']
    date_hierarchy = 'created_at'
    search_fields = ['product__name']
    autocomplete_fields = ['product']
    # raw_id_fields = ['product', 'vendor_store']
    list_select_related = ['product']
    list_filter = ['created_at', 'updated_at']
