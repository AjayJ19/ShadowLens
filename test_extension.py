#!/usr/bin/env python3
"""
Chrome Extension Test Script
Tests the ShadowLens Chrome extension functionality
"""

import os
import json
import requests
from datetime import datetime

def test_extension_files():
    """Test if all required extension files exist"""
    
    print("🔧 Testing Chrome Extension Files")
    print("=" * 40)
    
    required_files = [
        "chrome-extension/manifest.json",
        "chrome-extension/content.js",
        "chrome-extension/popup.html",
        "chrome-extension/popup.js",
        "chrome-extension/background.js"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_manifest_json():
    """Test manifest.json validity"""
    
    print(f"\n📋 Testing Manifest.json")
    print("-" * 30)
    
    try:
        with open("chrome-extension/manifest.json", "r") as f:
            manifest = json.load(f)
        
        required_fields = [
            "manifest_version",
            "name", 
            "version",
            "description",
            "permissions",
            "host_permissions",
            "background",
            "content_scripts",
            "action"
        ]
        
        for field in required_fields:
            if field in manifest:
                print(f"✅ {field}: {manifest[field]}")
            else:
                print(f"❌ {field}: MISSING")
                return False
        
        print(f"✅ Manifest.json is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading manifest.json: {e}")
        return False

def test_backend_connection():
    """Test if backend is accessible from extension"""
    
    print(f"\n🔗 Testing Backend Connection")
    print("-" * 30)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ Backend health check: OK")
        else:
            print(f"❌ Backend health check: {response.status_code}")
            return False
        
        # Test analysis endpoint
        test_data = {
            "url": "https://test-edtech.com",
            "forms": [{
                "fields": [
                    {"name": "email", "type": "email", "sensitive": True}
                ]
            }],
            "text": "Test EdTech site",
            "images": [],
            "riskIndicators": []
        }
        
        response = requests.post(
            "http://localhost:5000/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis endpoint: OK")
            print(f"   Risk Score: {result.get('risk_score', 'N/A')}/10")
            print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
        else:
            print(f"❌ Analysis endpoint: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False

def test_content_script():
    """Test content script functionality"""
    
    print(f"\n📜 Testing Content Script")
    print("-" * 30)
    
    try:
        with open("chrome-extension/content.js", "r") as f:
            content = f.read()
        
        required_functions = [
            "ShadowLensScanner",
            "scanPage",
            "sendToBackend",
            "handleHighRiskSite"
        ]
        
        for func in required_functions:
            if func in content:
                print(f"✅ {func} function found")
            else:
                print(f"❌ {func} function missing")
                return False
        
        print("✅ Content script looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error reading content script: {e}")
        return False

def test_popup():
    """Test popup functionality"""
    
    print(f"\n🪟 Testing Popup")
    print("-" * 30)
    
    try:
        with open("chrome-extension/popup.html", "r") as f:
            html = f.read()
        
        with open("chrome-extension/popup.js", "r") as f:
            js = f.read()
        
        required_elements = [
            "total-scans",
            "high-risk",
            "scan-current"
        ]
        
        for element in required_elements:
            if element in html or element in js:
                print(f"✅ {element} element found")
            else:
                print(f"❌ {element} element missing")
                return False
        
        print("✅ Popup looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error reading popup files: {e}")
        return False

def generate_extension_summary():
    """Generate extension summary"""
    
    print(f"\n📊 Extension Summary")
    print("=" * 30)
    
    summary = {
        "name": "ShadowLens - EdTech Privacy Guardian",
        "version": "1.0.0",
        "description": "Protects students by detecting privacy threats and brand impersonation in EdTech platforms",
        "features": [
            "Real-time privacy threat detection",
            "Form field analysis",
            "Brand impersonation detection", 
            "Risk scoring (1-10 scale)",
            "Consent banner",
            "Popup dashboard",
            "Offline analysis capability"
        ],
        "permissions": [
            "activeTab",
            "storage", 
            "scripting",
            "tabs"
        ],
        "host_permissions": [
            "http://localhost:5000/*",
            "https://*.edu/*",
            "https://*.school/*",
            "https://*.education/*"
        ]
    }
    
    for key, value in summary.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  • {item}")
        else:
            print(f"{key}: {value}")

def main():
    """Run all extension tests"""
    
    print("🔒 ShadowLens Chrome Extension Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Extension Files", test_extension_files),
        ("Manifest.json", test_manifest_json),
        ("Backend Connection", test_backend_connection),
        ("Content Script", test_content_script),
        ("Popup", test_popup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print(f"\n📈 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Extension is ready to load.")
        generate_extension_summary()
        
        print(f"\n📋 To load the extension in Chrome:")
        print("1. Open Chrome")
        print("2. Go to chrome://extensions/")
        print("3. Enable 'Developer mode'")
        print("4. Click 'Load unpacked'")
        print("5. Select the chrome-extension/ folder")
        print("6. Visit an EdTech site to test")
        
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main() 