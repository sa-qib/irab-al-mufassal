import json
import re
from django.core.management.base import BaseCommand
from pathlib import Path
from django.conf import settings

DATA_DIR = Path(settings.BASE_DIR) / "data"

class Command(BaseCommand):
    help = "Convert each surah's ayah.txt files into one JSON per surah"
    
    
    def parse_ayah_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            self.stdout.write(self.style.WARNING(f"⚠️ Skipping empty file: {file_path.name}"))
            return None

        # Expecting: "1 - Ayah text"
        match = re.match(r"(\d+)\s*-\s*(.+)", lines[0])
        if not match:
            self.stdout.write(self.style.WARNING(f"⚠️ Skipping invalid ayah header in: {file_path.name}"))
            return None

        ayah_number = int(match.group(1))
        ayah_text = match.group(2)

        parts = []
        for line in lines[1:]:
            if ':' in line:
                split_index = line.index(':')
                part_text = line[:split_index].strip()
                description = line[split_index + 1:].strip()
                parts.append({
                    "text": part_text,
                    "description": description
                })
            else:
                # Continuation of previous part description
                if parts:
                    parts[-1]["description"] += ' ' + line

        return {
            "ayah_number": ayah_number,
            "ayah_text": ayah_text,
            "parts": parts
        }

    def process_surah_folder(self, surah_folder, output_json_path):
        all_ayahs = []

        for file in sorted(surah_folder.glob("*.txt")):
            ayah_data = self.parse_ayah_file(file)
            if ayah_data:
                all_ayahs.append(ayah_data)

        if not all_ayahs:
            self.stdout.write(self.style.WARNING(f"⚠️ No valid ayahs found in {surah_folder.name}, skipping JSON export."))
            return

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(all_ayahs, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"✅ Saved: {output_json_path.name}"))


    def handle(self, *args, **kwargs):
        # === Main logic ===
        data_path = DATA_DIR / "seperate_surah_ayah_data"
        OUTPUT_JSON_DATA = DATA_DIR / "quran"
        OUTPUT_JSON_DATA.mkdir(exist_ok=True)
        
        if not data_path.is_dir():
            self.stderr.write("❌ 'seperate_surah_ayah_data' directory not found.")
            return

        for surah_folder in sorted(data_path.iterdir()):
            if surah_folder.is_dir():
                # Optional: make filename safe
                surah_name = surah_folder.name.replace(" ", "-")
                output_json_path = OUTPUT_JSON_DATA / f"{surah_name}.json"
                self.process_surah_folder(surah_folder, output_json_path)


