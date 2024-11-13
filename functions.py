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
