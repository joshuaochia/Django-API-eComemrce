from django.contrib import admin
from .models import (
    Product, ProductImage, ProductVariant,
    ProductReview, Categories, ProductTag
    )


class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    class Meta:
        model = ProductVariant


admin.site.register(ProductImage)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(Categories)
admin.site.register(ProductTag)
