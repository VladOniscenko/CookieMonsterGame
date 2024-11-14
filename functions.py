"""
HEY, lets store all static functions inside this file.
"""

import os
import sys
import pygame

def get_asset_path(asset_type:str, name:str):
    # For the deployed version (PyInstaller)
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

    # If running in the development environment, use the current working directory
    if not hasattr(sys, '_MEIPASS'):
        assets_path = os.path.join(os.getcwd(), 'assets', asset_type)
    else:
        # If running as a bundled executable, use the _MEIPASS path
        assets_path = os.path.join(base_path, 'assets', asset_type)

    return os.path.join(assets_path, name)


def get_image(name:str):
    # Use the helper function to get the correct path for the image
    path = get_asset_path('Other', name)

    # Load the image
    return pygame.image.load(path)


def split_text(text, font, font_size, max_width) -> str:
    """Breaks the text into multiple lines that fit within the given width."""
    font = pygame.font.Font(font, font_size)
    lines = []
    current_line = ''

    for word in text.split(' '):
        # Create a test line to check the width
        test_line = f"{current_line} {word}".strip()
        test_surface = font.render(test_line, True, (139, 0, 0))

        # If the line exceeds the max width, push the current line to lines and start a new one
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    return lines