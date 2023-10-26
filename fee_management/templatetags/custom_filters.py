# custom_filters.py

from django import template

register = template.Library()

@register.filter
def calculate_remaining_amount(total_semester_fee, total_paid_amount):
    if total_semester_fee is not None and total_paid_amount is not None:
        return total_semester_fee - total_paid_amount
    else:
        return None  # or some default value if needed
