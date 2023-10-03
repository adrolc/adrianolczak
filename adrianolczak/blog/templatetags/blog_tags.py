import markdown
from django import template
from django.utils.safestring import mark_safe
from taggit.models import Tag

from ..models import Post

register = template.Library()


@register.inclusion_tag("blog/includes/tt_latest_posts.html")
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.inclusion_tag("blog/includes/tt_all_tags.html")
def show_all_tags():
    tags = Tag.objects.all()
    return {"tags": tags}


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(
        markdown.markdown(
            text,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.extra",
                "markdown.extensions.attr_list",
            ],
        )
    )
