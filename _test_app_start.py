"""Quick test to see if app can start"""
import sys
print("Python version:", sys.version)
print("Starting import test...")

try:
    from flask import Flask
    print("[OK] Flask imported")

    from flask_socketio import SocketIO
    print("[OK] SocketIO imported")

    from core.config_manager import ConfigManager
    print("[OK] ConfigManager imported")

    from core.data_parser import DataParser
    print("[OK] DataParser imported")

    print("\n[OK] All imports successful!")
    print("\nNow attempting to start Flask app...")

    # Try to import the actual app
    import app
    print("[OK] App module imported successfully")

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
