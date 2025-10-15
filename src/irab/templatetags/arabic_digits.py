from django import template

register = template.Library()

@register.filter
def to_arabic_digits(value):
    if value is None:
        return ""
    arabic_nums = "٠١٢٣٤٥٦٧٨٩"
    result = ""
    for d in str(value):
        if d.isdigit():
            result += arabic_nums[int(d)]
        else:
            result += d
    return result
