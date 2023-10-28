# converters.py

from django.urls import converters

class FloatConverter:
    regex = r'[-+]?[0-9]*\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

converters.register_converter(FloatConverter, 'float')
