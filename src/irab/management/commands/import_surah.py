import json
from django.core.management.base import BaseCommand
from irab.models import Surah, Ayah, AyahPart
from pathlib import Path
from django.conf import settings

DATA_DIR = Path(settings.BASE_DIR) / "data" / "quran"


class Command(BaseCommand):
    help = "Import or update ayah and part data for each surah"

    def handle(self, *args, **options):
        for file in DATA_DIR.iterdir():
            if not file.name.endswith(".json"):
                continue  # skip non-JSON files

            try:
                surah_number = int(file.stem.split("-")[0])  # e.g. "1-surah-name.json"
            except ValueError:
                self.stderr.write(f"❌ Invalid filename: {file.name}")
                continue

            try:
                surah = Surah.objects.get(surah_id=surah_number)
            except Surah.DoesNotExist:
                self.stderr.write(f"❌ Surah with surah_id={surah_number} not found.")
                continue

            file_path = DATA_DIR / file.name
            with file_path.open(encoding="utf-8") as f:
                ayah_data = json.load(f)

            self.stdout.write(f"\n📖 Updating Surah {surah_number}: {surah.en_name}")

            for ayah_entry in ayah_data:
                ayah_number = ayah_entry["ayah_number"]
                ayah_text = ayah_entry["ayah_text"]
                parts_data = ayah_entry.get("parts", [])

                # Get or create the Ayah
                ayah, created = Ayah.objects.get_or_create(
                    surah=surah,
                    ayah_number=ayah_number,
                    defaults={"ayah_text": ayah_text},
                )

                # Update text if changed
                if not created and ayah.ayah_text != ayah_text:
                    ayah.ayah_text = ayah_text
                    ayah.save()
                    self.stdout.write(f"🔁 Updated Ayah text for {ayah_number}")

                # Compare existing parts vs new parts
                existing_parts = list(ayah.parts.values("part", "description"))
                new_parts = [
                    {"part": p["text"], "description": p["description"]}
                    for p in parts_data
                ]

                if existing_parts != new_parts:
                    ayah.parts.all().delete()
                    for part in new_parts:
                        AyahPart.objects.create(
                            ayah=ayah,
                            part=part["part"],
                            description=part["description"],
                        )
                    self.stdout.write(
                        f"   ↳ Updated {len(new_parts)} part(s) for Ayah {ayah_number}"
                    )
                else:
                    self.stdout.write(f"⚠️ Ayah {ayah_number} unchanged")

            self.stdout.write(f"✅ Finished updating Surah {surah_number}")
