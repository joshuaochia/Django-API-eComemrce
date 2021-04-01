from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
    )
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django_countries.fields import CountryField
from products.models import ProductVariant
# from colorfield import fields


class UserManager(BaseUserManager):

    """
    Creates and save a User with the given email,
    username, firstname, lastname, and password.
    """

    # Create User
    def create_user(
        self, username, email,
        first_name, last_name,
        password=None
            ):

        # check if there's username and email
        if not email and username:
            raise ValueError('User must have an email and username')

        # Create a user using the params of create_user
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        # set password then hash it and saving the new model
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create super user
    def create_superuser(
        self, username, email,
        first_name, last_name, password
            ):

        # using the create_user function to create new user
        user = self.create_user(
            username, email, first_name,
            last_name, password
            )

        # setting the new user to admin and superuser
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        # saving the changes and returning it
        user.save(using=self._db)
        return User


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User """

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    username = models.CharField(max_length=55, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    """ Fields """
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    """ Creating user Handler """
    objects = UserManager()

    def __str__(self):
        # string representation for DB
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        # User permission
        return True

    def has_module_perms(self, app_label):
        # User permission to view the ap modules
        return True


class Profile(models.Model):

    """ Separate Profile for security """
    profile = models.ImageField(upload_to='profile_pics/')
    slug = models.SlugField()
    user = models.OneToOneField(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='profiles'
                )
    full_name = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    cart_cost = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.full_name = f'{self.user.first_name} {self.user.last_name}'
        self.slug = slugify(self.user.username)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ProfileCartManager(models.Manager):
    """ Managing cart item when created"""

    def create(self, profile, product, quantity, cost,):

        # Add the new cost to user current cart cost.
        money = cost * quantity
        profile.cart_cost += money

        # create the cart
        cart = self.model(
            profile=profile,
            product=product,
            quantity=quantity,
            cost=cost
        )

        # saving both changes
        profile.save()
        cart.save(using=self._db)

        return cart


class ProfileProductCart(models.Model):
    """ Creating a cart item specific for one product """
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_p',
        null=True
        )
    quantity = models.PositiveSmallIntegerField()
    cost = models.PositiveSmallIntegerField()

    objects = ProfileCartManager()


# Create a profile instance after the user is created
@receiver(post_save, sender=User)
def after_user_created(sender, instance, created, **kwargs):
    profile = Profile()
    profile.user = instance
    profile.slug = instance.username
    profile.first_name = instance.first_name
    profile.last_name = instance.last_name
    profile.save()


class Address(models.Model):
    """ Address connected to single user """
    # Different address may apply for buying products
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='user_address'
                )
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255)
    country = CountryField()
    zip_code = models.IntegerField()
    default = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} Address'
