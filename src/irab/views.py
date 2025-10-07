from django.shortcuts import render
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent.parent
DATA_FILE = BASE / "data" / "110-Surah-Nasr.json"

def home_page(request):
    return render(request, "pages/home.html")


def surah_page(request):
    return render(request, "pages/surah.html")


def test_page(request, *args, **kwargs):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        surah_data = json.load(f)
    
    ayah_count = len(surah_data)
    context = {
        "surah_data": surah_data,
        "ayah_count": ayah_count
    }
    return render(request,"test.html", context)