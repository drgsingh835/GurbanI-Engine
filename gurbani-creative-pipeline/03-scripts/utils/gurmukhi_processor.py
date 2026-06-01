import os
from PIL import Image, ImageDraw, ImageFont

try:
    from gurmukhiutils.unicode import unicode as g_unicode
    from gurmukhiutils.ascii import ascii as g_ascii
except ImportError:
    # Fallback to dummy implementation if library not installed yet
    g_unicode = None
    g_ascii = None

class GurmukhiProcessor:
    """
    Base Gurmukhi text processor.
    Provides standard Unicode normalization and Legacy ASCII conversion for artistic fonts.
    """
    
    @staticmethod
    def is_punjabi(text: str) -> bool:
        """Checks if the text contains Gurmukhi/Punjabi characters."""
        if not text:
            return False
        return any('\u0a00' <= char <= '\u0a7f' for char in text)
    
    @staticmethod
    def normalize(text: str) -> str:
        """Standard Unicode normalization."""
        if not text: 
            return ""
        if GurmukhiProcessor.is_punjabi(text):
            if g_unicode:
                return g_unicode(text)
        return text

    @staticmethod
    def to_legacy_ascii(text: str) -> str:
        """Converts to AmrLipi-compatible ASCII."""
        if not text: 
            return ""
        if g_ascii:
            normalized = GurmukhiProcessor.normalize(text)
            return g_ascii(normalized)
        return text
