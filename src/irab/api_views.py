from django.shortcuts import render, get_object_or_404, redirect
from irab.models import Surah, Ayah
from django.views.decorators.http import require_GET
from django.db.models import Q
import re


def search(request):
    query= request.GET.get("q", "").strip().lower()
    
    if not query:
        return redirect("home")
    
    
    pattern = r"^(?P<surah>[a-zA-Z\-]+|\d+)(?:[\s:](?P<ayah>\d+))?$"
    match = re.match(pattern, query)
    
    if not match:
        return redirect("home")
    
    surah = match.group('surah')
    ayah = match.group('ayah')
    
    if ayah:
        return redirect('ayah_page', identifier=surah, ayah_number=ayah)
    else:
        return redirect('surah_detail', identifier=surah)
    
    
    