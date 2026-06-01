import os
from PIL import Image, ImageDraw, ImageFont
from gurmukhiutils.unicode import unicode as g_unicode
from gurmukhiutils.ascii import ascii as g_ascii

class GurmukhiProcessor:
    """
    Base Gurmukhi text processor for Punjabi Guftar.
    Provides standard Unicode normalization and Legacy ASCII conversion for artistic fonts.
    No manual character nudging.
    """
    
    @staticmethod
    def normalize(text: str) -> str:
        """Standard Unicode normalization."""
        if not text: return ""
        if any('\u0a00' <= char <= '\u0a7f' for char in text):
            return g_unicode(text)
        return text

    @staticmethod
    def to_legacy_ascii(text: str) -> str:
        """Converts to AmrLipi-compatible ASCII."""
        if not text: return ""
        normalized = GurmukhiProcessor.normalize(text)
        return g_ascii(normalized)
