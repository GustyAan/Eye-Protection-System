# config.py
import os

# Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Database configuration
DB_PATH = os.path.join(DATA_DIR, 'eye_protection.db')

# Application settings
SCREEN_TIME_LIMIT = 20  # seconds
BREAK_TIME_REQUIRED = 7  # seconds
DETECTION_INTERVAL = 1  # seconds

# Developer password
DEV_PASSWORD = "Kakikudaada4"

# UI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LOGO_PATH = os.path.join(ASSETS_DIR, 'pens_logo.png')

# Cascade classifier path
CASCADE_PATH = os.path.join(MODELS_DIR, 'haarcascade_frontalface_default.xml')