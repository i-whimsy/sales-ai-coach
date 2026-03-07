import sys
try:
    print("Attempting to import main module...")
    from main import app
    print(f"Import successful! App has {len(app.routes)} routes.")
    print("Routes found:")
    for route in app.routes:
        if "models" in route.path:
            print(f"  - {route.path}")
except Exception as e:
    print(f"Import failed with error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
