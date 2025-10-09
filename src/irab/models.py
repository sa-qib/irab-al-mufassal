from django.db import models

# Create your models here.

class Surah(models.Model):
    surah_id = models.PositiveIntegerField(unique=True)
    ar_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    translated_name = models.CharField(max_length=250, null=True, blank=True)
    revelation_place = models.CharField(max_length=10,  choices=[("makkah", "Makkah"), ("madinah", "Madinah")])
    verses_count = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.id} - {self.en_name}"
    
    
    
class Ayah(models.Model):
    surah = models.ForeignKey(Surah, related_name="ayahs", on_delete=models.CASCADE)
    ayah_number = models.IntegerField()
    ayah_text = models.TextField()
    
    
    def __str__(self):
        # return f"{self.surah.id}:{self.ayah_number} - {self.ayah_text[:30]}"
        return f"{self.surah.en_name} : {self.ayah_number}"
    
    
class AyahPart(models.Model):
    ayah = models.ForeignKey(Ayah, related_name="parts", on_delete=models.CASCADE)
    part = models.CharField(max_length=250)
    description = models.TextField()

    
    def __str__(self):
        return f"{self.ayah} - ({self.part})"