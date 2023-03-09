from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class HomepageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return ['homepage:home']
    
    def location(self, item):
        return reverse(item)