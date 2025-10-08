from django.shortcuts import render
from django.http import Http404
from pathlib import Path
import json
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "json_data"
surah_metadata = BASE / "data/surah_metadata.json"

def home_page(request):
    # context =defaultdict()
    # surah_names = defaultdict(list)
    # if DATA_DIR.is_dir():
    #     for file in sorted(DATA_DIR.glob("*.json")):
    #         if "-" in file.stem:
    #             parts = file.stem.split("-")
    #             if len(parts) >= 3:
    #                 surah_name = "-".join(parts[2:])
    #             else:
    #                 surah_name = "-".join(parts[1:])
    #         context["surah_name"].append(surah_name)
                    
    with open(surah_metadata, mode="r", encoding="utf-8") as file:
        data = json.load(file)
    context = {"data": data}
    return render(request, "pages/home.html", context)

def surah_page(request):
    return render(request, "pages/surah.html")



def test_page(request, *args, **kwargs):
    with open(surah_metadata, mode="r", encoding="utf-8") as file:
        data = json.load(file)
    context = {"data": data}
    return render(request, "test2.html", context)



# def test_surah(request, identifier):
#     identifier = identifier.strip().lower()

#     # Normalize numeric identifiers like "1", "01", "001"
#     if identifier.isdigit():
#         identifier = str(int(identifier)).zfill(3)
        
#     # Try to find file that matches either number or name
#     matched_file = None
#     for file in DATA_DIR.glob("*.json"):
#         name = file.stem.lower()
#         if identifier in name or name.startswith(identifier):
#             matched_file = file
#             break
        
#     if not matched_file:
#         raise Http404("Surah not found")

#     # Load JSON data
#     with open(matched_file, "r", encoding="utf-8") as f:
#         surah_data = json.load(f)

#     return render(request, "surah_detail.html", {"surah_data": surah_data})