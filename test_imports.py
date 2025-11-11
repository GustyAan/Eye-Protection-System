try:
    import cv2
    import tkinter
    import matplotlib
    from PIL import Image
    import sqlite3
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")