from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class CoreSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
          'core:index',
        ]

    def location(self, item):
        return reverse(item)
