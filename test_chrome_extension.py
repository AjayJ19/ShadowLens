#!/usr/bin/env python3
"""
Test ShadowLens Chrome Extension Setup
"""

import os
import json

def check_extension_files():
    """Check if all required extension files exist"""
    print("🔍 Checking Chrome Extension Files...")
    
    required_files = [
        'chrome-extension/manifest.json',
        'chrome-extension/popup.html',
        'chrome-extension/popup.js',
        'chrome-extension/content.js',
        'chrome-extension/background.js',
        'chrome-extension/icons/icon16.png',
        'chrome-extension/icons/icon32.png',
        'chrome-extension/icons/icon48.png',
        'chrome-extension/icons/icon128.png'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("\n✅ All extension files present!")
        return True

def check_manifest():
    """Check if manifest.json is valid"""
    print("\n🔍 Checking manifest.json...")
    
    try:
        with open('chrome-extension/manifest.json', 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['manifest_version', 'name', 'version', 'permissions', 'content_scripts']
        missing_fields = []
        
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing manifest fields: {missing_fields}")
            return False
        else:
            print("✅ Manifest.json is valid!")
            print(f"   📦 Extension: {manifest['name']}")
            print(f"   📋 Version: {manifest['version']}")
            print(f"   🔧 Permissions: {len(manifest['permissions'])}")
            return True
            
    except Exception as e:
        print(f"❌ Error reading manifest.json: {e}")
        return False

def check_backend():
    """Check if backend server is running"""
    print("\n🔍 Checking Backend Server...")
    
    try:
        import requests
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running!")
            return True
        else:
            print(f"❌ Backend server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend server is not running: {e}")
        print("💡 Start the backend with: python3 backend/app.py")
        return False

def main():
    print("🔒 ShadowLens Chrome Extension Test")
    print("=" * 50)
    
    # Check files
    files_ok = check_extension_files()
    
    # Check manifest
    manifest_ok = check_manifest()
    
    # Check backend
    backend_ok = check_backend()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Files: {'✅' if files_ok else '❌'}")
    print(f"   Manifest: {'✅' if manifest_ok else '❌'}")
    print(f"   Backend: {'✅' if backend_ok else '❌'}")
    
    if files_ok and manifest_ok and backend_ok:
        print("\n🎉 All tests passed! Chrome extension is ready to use.")
        print("\n📋 Next steps:")
        print("1. Open Chrome and go to chrome://extensions/")
        print("2. Enable 'Developer mode'")
        print("3. Click 'Load unpacked'")
        print("4. Select the 'chrome-extension' folder")
        print("5. Visit any website and click the ShadowLens icon!")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main() 