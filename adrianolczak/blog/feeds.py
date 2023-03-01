import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Tech Blog - adrianolczak.pl'
    link = reverse_lazy('blog:home')
    description = 'New posts of Tech Blog - adrianolczak.pl'

    def items(self):
        return Post.published.all()[:4]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body, extensions=['markdown.extensions.fenced_code']), 35)

    def item_pubdate(self, item):
        return item.publish