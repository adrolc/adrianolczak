from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from .storage import OverwriteStorage, post_content_images_path, post_image_path

User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    photo = models.ImageField(upload_to=post_image_path, storage=OverwriteStorage())
    body = models.TextField()
    github_link = models.URLField(blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    objects = models.Manager()  # Default manager.
    published = PublishedManager()  # published manager (internal).
    tags = TaggableManager()  # Taggit manager (external).

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=post_content_images_path)
