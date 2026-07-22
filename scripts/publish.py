import os
import shutil
import subprocess
import sys

def main():
    print("==================================================")
    print("   OpenStockAPI — PyPI Release Automation Tool   ")
    print("==================================================")

    # Move to root directory if running inside scripts/
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(root_dir)

    # 1. Clean old build artifacts
    for folder in ["dist", "build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"-> Cleared old {folder}/ directory")

    # 2. Build package
    print("\n[1/3] Building package (python -m build)...")
    res = subprocess.run([sys.executable, "-m", "build"])
    if res.returncode != 0:
        print("[ERR] Build failed!")
        sys.exit(1)

    # 3. Check package
    print("\n[2/3] Checking package (python -m twine check dist/*)...")
    res = subprocess.run([sys.executable, "-m", "twine", "check", "dist/*"])
    if res.returncode != 0:
        print("[ERR] Twine check failed!")
        sys.exit(1)

    # 4. Upload to PyPI
    print("\n[3/3] Uploading package to PyPI (python -m twine upload dist/*)...")
    res = subprocess.run([sys.executable, "-m", "twine", "upload", "dist/*"])
    if res.returncode != 0:
        print("[ERR] Upload failed!")
        sys.exit(1)

    print("\n[OK] Successfully published new version to PyPI!")

if __name__ == "__main__":
    main()
