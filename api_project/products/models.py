from django.db import models
from django.utils.text import slugify
from django.conf import settings


categories = (
    ('electronic-devices', 'Electronic Devices'),
    ('home-Living', 'Home & Living'),
    ('health-beauty', 'Health & Beauty'),
    ('babies-toys', 'Babies Toys'),
    ("men-fashion", "Men's Fashion"),
    ("women-Fashion", "Women's Fashion"),

)


class Categories(models.Model):
    name = models.CharField(choices=categories, max_length=55, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    time_posted = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='products'
        )
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):

    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        null=True
        )
    specification = models.CharField(max_length=555)
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class ProductImage(models.Model):

    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='img',
        null=True, blank=True
        )
    image = models.ImageField(upload_to='products/', null=True, blank=True)


class ProductTag(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    tag = models.CharField(max_length=55)

    def __str__(self):

        return self.tag


class ProductReview(models.Model):

    stars = (
        (1, ('1 Star')),
        (2, ('2 Stars')),
        (3, ('3 Stars')),
        (4, ('4 Stars')),
        (5, ('5 Stars')),

    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    star = models.PositiveSmallIntegerField(choices=stars, default=1)
    review = models.CharField(max_length=255)
    rv_img = models.ImageField(upload_to='reviews/', null=True, blank=True)
