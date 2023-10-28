# custom_filters.py

from django import template

register = template.Library()

@register.filter
def calculate_remaining_amount(total_semester_fee, total_paid_amount):
    return total_semester_fee - total_paid_amount
