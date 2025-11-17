import importlib, traceback, os
print("cwd=", os.getcwd())
try:
    import app.main
    print("IMPORT OK")
except Exception:
    traceback.print_exc()
