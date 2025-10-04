from django.shortcuts import render



def home_page(request):
    return render(request, "pages/home.html")


def surah_page(request):
    return render(request, "pages/surah.html")