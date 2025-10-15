from django import template

register = template.Library()

@register.filter
def to_arabic_digits(value):
    try:
        mapping = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
        return str(value).translate(mapping)
    except Exception:
        return value  # fallback if something goes wrong
