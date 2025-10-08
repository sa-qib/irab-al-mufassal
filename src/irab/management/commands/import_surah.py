import json 
from django.core.management.base import BaseCommand
from irab.models import Surah
from pathlib import Path
from django.conf import settings

DATA_DIR = Path(settings.BASE_DIR) / "data"

class Command(BaseCommand):
    help = "Import surah metadata from JSON file"
    
    def handle(self, *args, **options):
        path = DATA_DIR / "surah_metadata.json"  # adjust path if needed
        
        if not path.exists():
            self.stderr.write("JSON file not found.")
            return

        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        for surah_id, info in data.items():
            surah, created = Surah.objects.get_or_create(
                id=int(surah_id),
                defaults={
                    "surah_id": int(surah_id),
                    "ar_name": info.get("ar_name", ""),
                    "en_name": info.get("en_name", ""),
                    "translated_name": info.get("translatedName", ""),
                    "revelation_place": info.get("revelationPlace", ""),
                    "verses_count": int(info.get("versesCount", 0))
                }
            )
            if created:
                self.stdout.write(f"Added Surah {surah_id} - {surah.en_name}")
            else:
                self.stdout.write(f"Surah {surah_id} already exists")