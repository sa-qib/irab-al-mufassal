from django.urls import path, re_path
from irab import views, api_views



urlpatterns = [
    path('', views.home_page, name="home"),
    path('contact/', views.contact_page, name="contact"),
    path('<str:identifier>/', views.surah_page, name="surah_detail"),
    re_path(r'^(?P<identifier>[\w-]+)/(?P<ayah_number>\d{1,3})/$', views.ayah_page, name='ayah_page'),
    path('api/search/', api_views.search, name="search"),
]
