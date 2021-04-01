from core.models import Profile
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Blog(models.Model):

    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True
        )
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=55)
    body = RichTextField()
    thumbnail = models.ImageField(
        blank=True,
        null=True,
        upload_to='blog_thumbnail/'
    )
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class BlogComment(models.Model):

    blog = models.ForeignKey(
        Blog,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True
    )
    comment = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.profile)
