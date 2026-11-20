from django import template

register = template.Library()

EN_TO_FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


@register.filter
def fa_digits(value):
    if value is None:
        return ""
    return str(value).translate(EN_TO_FA)


@register.filter
def toman(value):
    try:
        formatted = f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)
    return formatted.translate(EN_TO_FA)
