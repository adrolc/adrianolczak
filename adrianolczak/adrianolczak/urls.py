from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.static import serve
from homepage.sitemaps import HomepageSitemap

sitemaps = {
    "posts": PostSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # Available after executing collectstatic
    path(
        "robots.txt",
        serve,
        {"document_root": settings.STATIC_ROOT, "path": "robots.txt"},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
