from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Surah

class StaticViewSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0
    def items(self):
        return ["home"]
    
    def location(self,item):
        return reverse(item)
    
    
class SurahSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        return Surah.objects.all()

    def location(self, obj):
        return reverse('surah_detail', args=[obj.en_name])