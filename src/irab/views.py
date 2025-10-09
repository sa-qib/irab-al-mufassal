from django.shortcuts import render, get_object_or_404
from django.http import Http404
from pathlib import Path
from irab.models import Surah
from fontTools.ttLib import TTFont
from django.conf import settings

BASE_DIR = Path(settings.BASE_DIR)
DATA_DIR = BASE_DIR / "json_data"
surah_metadata = BASE_DIR / "data/surah_metadata.json"
font_path = BASE_DIR / 'static/fonts/sura_names.ttf'


def get_surah_glyphs(ttf_path):
    font = TTFont(ttf_path)
    glyphs = []
    for table in font['cmap'].tables:
        for code in sorted(table.cmap.keys()):
            if code >= 0xE000:
                glyphs.append(chr(code))
    return glyphs


def home_page(request):
    surahs = Surah.objects.order_by("surah_id")
    glyphs = get_surah_glyphs(font_path)  # path to your font file

    surah_data = []
    for idx, surah in enumerate(surahs):
        # Fallback if not enough glyphs
        glyph = glyphs[idx] if idx < len(glyphs) else None

        if glyph == '\ue000':
            display_text = surah.ar_name  # Use Arabic name for first entry
        else:
            display_text = glyph

        surah_data.append({
            "surah": surah,
            "glyph": display_text
        })
        context = {
            "surah_data": surah_data
        }
    return render(request, "pages/home.html", context)



def surah_page(request,identifier,ayah_number=None, *args, **kwargs):
    if identifier.isdigit():
        # If identifier is digits only, treat as surah_number
        surah = get_object_or_404(Surah, surah_id=int(identifier))
    else:
        # Otherwise treat as slug / en_name
        surah = get_object_or_404(Surah, en_name=identifier)
    return render(request, "pages/surah.html", {
        "surah": surah,
        "scroll_to_ayah": ayah_number
    })
    


def ayah_page(request,identifier,ayah_number):
    if identifier.isdigit():
        # If identifier is digits only, treat as surah_number
        surah = get_object_or_404(Surah, surah_id=int(identifier))
    else:
        # Otherwise treat as slug / en_name
        surah = get_object_or_404(Surah, en_name=identifier)
    
    ayah = get_object_or_404(surah.ayahs, ayah_number=ayah_number)
    return render(request, "pages/ayah_page.html", {
       "surah": surah,
        "ayah": ayah,
        "scroll_to_ayah": ayah_number
    })