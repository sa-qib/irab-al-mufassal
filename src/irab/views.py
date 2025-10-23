from django.shortcuts import render,redirect, get_object_or_404
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



def surah_page(request, identifier, ayah_number=None, *args, **kwargs):
    # Fetch all surahs for sidebar/navigation
    surahs = Surah.objects.all().order_by('surah_id')

    # Determine if identifier is a number or name
    if identifier.isdigit():
        surah = Surah.objects.filter(surah_id=int(identifier)).first()
        if not surah:
            raise Http404("Surah not found")
        # Redirect to canonical name-based URL
        return redirect('surah_detail', identifier=surah.en_name.lower())

    # Otherwise, fetch by English name
    surah = Surah.objects.filter(en_name=identifier.lower()).first()
    if not surah:
        raise Http404("Surah not found")

    # 🕓 If surah exists but has no ayahs, show 'coming soon'
    if not surah.ayahs.exists():
        return render(request, "pages/surah.html", {
            "surahs": surahs,
            "surah": surah,
            "coming_soon": True
        })

    # ✅ Normal render
    return render(request, "pages/surah.html", {
        "surahs": surahs,
        "surah": surah,
        "scroll_to_ayah": ayah_number
    })
    



def ayah_page(request, identifier, ayah_number):
    # Get surah by ID or name
    if identifier.isdigit():
        surah = Surah.objects.filter(surah_id=int(identifier)).first()
    else:
        surah = Surah.objects.filter(en_name=identifier).first()

    if not surah:
        raise Http404("Surah not found")

    # If no ayahs yet → coming soon page
    if not surah.ayahs.exists():
        return render(request, "pages/surah.html", {
            "surah": surah,
            "coming_soon": True
        })

    # Validate ayah number range
    try:
        ayah_number = int(ayah_number)
    except ValueError:
        raise Http404("Invalid ayah number")

    if ayah_number < 1 or ayah_number > surah.verses_count:
        raise Http404("Ayah not found")

    # Get ayah
    ayah = surah.ayahs.filter(ayah_number=ayah_number).first()
    if not ayah:
        # If ayah doesn’t exist in DB (maybe not added yet)
        raise Http404("Ayah not found")

    # Render ayah page
    return render(request, "pages/ayah_page.html", {
        "surah": surah,
        "ayah": ayah,
        "scroll_to_ayah": ayah_number
    })


def custom_404_view(request, exception):
    return render(request, "pages/404.html", status=404)



def contact_page(request, *args, **kwargs):
    surahs = Surah.objects.all()
    context = {
        "surahs": surahs
    }
    
    return render(request, "pages/contact.html", context)