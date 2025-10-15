import json 
from django.core.management.base import BaseCommand
from irab.models import Surah, Ayah, AyahPart
from pathlib import Path
from django.conf import settings

DATA_DIR = Path(settings.BASE_DIR) / "data" / "quran"

class Command(BaseCommand):
    help = "Import ayah and part data for each surah"

    def handle(self, *args, **options):
        for file in DATA_DIR.iterdir():
            if not file.name.endswith(".json"):
                continue  # skip non-JSON files
            
            try:
                surah_number = int(file.stem.split("-")[0])  # e.g. "1-surah-name.json"
            except ValueError:
                self.stderr.write(f"❌ Invalid filename: {file.name}")
                continue

            file_path = DATA_DIR / file.name

            with file_path.open(encoding="utf-8") as f:
                ayah_data = json.load(f)

            try:
                surah = Surah.objects.get(surah_id=surah_number)
            except Surah.DoesNotExist:
                self.stderr.write(f"❌ Surah with surah_id={surah_number} not found.")
                continue

            self.stdout.write(f"\n📖 Importing Surah {surah_number}: {surah.en_name}")

            for ayah_entry in ayah_data:
                ayah_number = ayah_entry["ayah_number"]
                ayah_text = ayah_entry["ayah_text"]

                # Get or create the Ayah
                ayah, created = Ayah.objects.get_or_create(
                    surah=surah,
                    ayah_number=ayah_number,
                    defaults={"ayah_text": ayah_text}
                )

                # 🧠 Skip if already imported and unchanged
                if not created and ayah.ayah_text == ayah_text and ayah.parts.exists():
                    self.stdout.write(f"⚠️ Skipping Ayah {ayah_number}, already imported.")
                    continue


                self.stdout.write(f"✅ Ayah {ayah_number}: {ayah_text[:40]}...")

                # Add Ayah Parts
                for part in ayah_entry.get("parts", []):
                    AyahPart.objects.create(
                        ayah=ayah,
                        part=part["text"],
                        description=part["description"]
                    )

                self.stdout.write(f"   ↳ Added {len(ayah_entry.get('parts', []))} part(s)")
