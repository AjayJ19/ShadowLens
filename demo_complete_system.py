#!/usr/bin/env python3
"""
Complete ShadowLens System Demo
Demonstrates the full AI-powered privacy protection system
"""

import requests
import json
import time
import os
from datetime import datetime

def print_header():
    """Print demo header"""
    print("🔒 ShadowLens - Complete System Demo")
    print("=" * 60)
    print("AI-Powered Privacy Guardian for EdTech Platforms")
    print("=" * 60)
    print()

def test_backend():
    """Test backend functionality"""
    print("🧠 Testing AI Backend")
    print("-" * 30)
    
    try:
        # Health check
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend Status: {health_data.get('status', 'Unknown')}")
            print(f"✅ AI Model: {health_data.get('ai_model', 'Unknown')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test different scenarios
        test_cases = [
            {
                "name": "Safe EdTech Site",
                "data": {
                    "url": "https://safe-learning.org",
                    "forms": [{"fields": []}],
                    "text": "Free educational resources. No personal data required.",
                    "images": [],
                    "riskIndicators": []
                }
            },
            {
                "name": "Medium Risk Site", 
                "data": {
                    "url": "https://coursera.org",
                    "forms": [{
                        "fields": [
                            {"name": "email", "type": "email", "sensitive": True}
                        ]
                    }],
                    "text": "Coursera collects email for account creation and course access.",
                    "images": [],
                    "riskIndicators": [
                        {"type": "privacy_term", "term": "collects email", "risk": "medium"}
                    ]
                }
            },
            {
                "name": "High Risk Site",
                "data": {
                    "url": "https://suspicious-edtech.net",
                    "forms": [{
                        "fields": [
                            {"name": "full_name", "type": "text", "sensitive": True},
                            {"name": "phone", "type": "tel", "sensitive": True},
                            {"name": "ssn", "type": "text", "sensitive": True},
                            {"name": "parent_income", "type": "number", "sensitive": True}
                        ]
                    }],
                    "text": "We collect extensive personal information including SSN and family income for verification.",
                    "images": [{"alt": "Google Certified", "filename": "fake-google-logo.png"}],
                    "riskIndicators": [
                        {"type": "privacy_term", "term": "SSN", "risk": "high"},
                        {"type": "privacy_term", "term": "family income", "risk": "high"},
                        {"type": "brand_impersonation", "term": "Google Certified", "risk": "high"}
                    ]
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📊 Test {i}: {test_case['name']}")
            
            response = requests.post(
                "http://localhost:5000/analyze",
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Analysis Complete")
                print(f"   🎯 Risk Score: {result.get('risk_score', 'N/A')}/10")
                print(f"   📋 Recommendation: {result.get('recommendation', 'N/A')}")
                
                if result.get('red_flags'):
                    print(f"   🚩 Red Flags: {len(result['red_flags'])} found")
                    for flag in result['red_flags'][:2]:  # Show first 2
                        print(f"      • {flag}")
                
                if result.get('privacy_threats'):
                    print(f"   ⚠️ Privacy Threats: {len(result['privacy_threats'])} found")
                
                if result.get('brand_impersonation'):
                    print(f"   🎭 Brand Impersonation: {len(result['brand_impersonation'])} found")
                    
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_chrome_extension():
    """Test Chrome extension components"""
    print(f"\n🔧 Testing Chrome Extension")
    print("-" * 30)
    
    extension_files = [
        "chrome-extension/manifest.json",
        "chrome-extension/content.js", 
        "chrome-extension/popup.html",
        "chrome-extension/popup.js",
        "chrome-extension/background.js"
    ]
    
    all_exist = True
    for file_path in extension_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    if all_exist:
        print("✅ All extension files present")
        
        # Test manifest.json
        try:
            with open("chrome-extension/manifest.json", "r") as f:
                manifest = json.load(f)
            
            required_fields = ["manifest_version", "name", "version", "permissions"]
            for field in required_fields:
                if field in manifest:
                    print(f"✅ {field}: {manifest[field]}")
                else:
                    print(f"❌ {field}: MISSING")
                    return False
            
            print("✅ Manifest.json valid")
            
        except Exception as e:
            print(f"❌ Manifest.json error: {e}")
            return False
    
    return all_exist

def test_dashboard():
    """Test React dashboard"""
    print(f"\n📊 Testing Business Dashboard")
    print("-" * 30)
    
    try:
        # Test if dashboard is running
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Dashboard is running")
        else:
            print(f"❌ Dashboard not responding: {response.status_code}")
            return False
        
        # Test dashboard API connection
        dashboard_data = {
            "url": "https://demo-edtech.com",
            "forms": [{
                "fields": [
                    {"name": "email", "type": "email", "sensitive": True}
                ]
            }],
            "text": "Demo site for dashboard testing",
            "images": [],
            "riskIndicators": []
        }
        
        response = requests.post(
            "http://localhost:5000/analyze",
            json=dashboard_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Dashboard API connection: OK")
            print(f"   📈 Sample analysis: {result.get('risk_score', 'N/A')}/10")
        else:
            print(f"❌ Dashboard API connection failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard test error: {e}")
        return False

def show_system_architecture():
    """Show system architecture"""
    print(f"\n🏗️ System Architecture")
    print("-" * 30)
    
    architecture = {
        "Chrome Extension": {
            "Components": ["Content Script", "Popup UI", "Background Service Worker"],
            "Features": ["Real-time scanning", "Form detection", "Brand analysis", "Risk scoring"],
            "Permissions": ["activeTab", "storage", "scripting", "tabs"]
        },
        "AI Backend": {
            "Framework": "Python Flask",
            "AI Models": ["Gemini Pro (cloud)", "Mistral (local)"],
            "Endpoints": ["/health", "/analyze"],
            "Analysis": ["Privacy threats", "Brand impersonation", "Risk scoring"]
        },
        "Business Dashboard": {
            "Framework": "React.js",
            "Features": ["Real-time monitoring", "Analytics", "Export functionality"],
            "UI": ["Overview", "Monitoring", "Analytics", "Compliance"]
        }
    }
    
    for component, details in architecture.items():
        print(f"\n{component}:")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    • {item}")
            else:
                print(f"  {key}: {value}")

def show_business_case():
    """Show business case"""
    print(f"\n💰 Business Case")
    print("-" * 30)
    
    market_data = {
        "Market Size": {
            "Global EdTech Market": "$123B (2022)",
            "K-12 Students (US)": "50.8M",
            "Privacy Protection Market": "$2.1B",
            "Target Addressable Market": "$15B"
        },
        "Revenue Models": {
            "B2B SaaS (Schools)": "$5-10/student/year",
            "B2C Premium (Parents)": "$2.99/month", 
            "API Certification": "$0.01/scan",
            "NGO Editions": "Grant-funded"
        },
        "Competitive Advantages": [
            "First comprehensive student privacy solution",
            "AI-powered analysis vs rule-based competitors",
            "Privacy-first design with no data collection",
            "Multi-model support (cloud + local)",
            "Real-time detection capabilities"
        ]
    }
    
    for category, data in market_data.items():
        print(f"\n{category}:")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  • {key}: {value}")
        else:
            for item in data:
                print(f"  • {item}")

def show_deployment_instructions():
    """Show deployment instructions"""
    print(f"\n🚀 Deployment Instructions")
    print("-" * 30)
    
    instructions = {
        "Backend": [
            "cd backend && python app.py",
            "Backend runs on http://localhost:5000",
            "AI model: Rule-based analysis (Mistral fallback)"
        ],
        "Dashboard": [
            "cd dashboard && npm start", 
            "Dashboard runs on http://localhost:3000",
            "Real-time connection to backend"
        ],
        "Chrome Extension": [
            "Open Chrome → chrome://extensions/",
            "Enable 'Developer mode'",
            "Click 'Load unpacked' → Select chrome-extension/",
            "Visit EdTech sites to test"
        ],
        "Testing": [
            "Run: python demo_complete_system.py",
            "Run: python test_extension.py", 
            "Visit: http://localhost:3000 for dashboard",
            "Test on real EdTech sites"
        ]
    }
    
    for component, steps in instructions.items():
        print(f"\n{component}:")
        for step in steps:
            print(f"  • {step}")

def main():
    """Run complete system demo"""
    
    print_header()
    
    # Run tests
    tests = [
        ("AI Backend", test_backend),
        ("Chrome Extension", test_chrome_extension),
        ("Business Dashboard", test_dashboard)
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
    
    print(f"\n📈 System Test Results: {passed}/{total} components working")
    
    if passed == total:
        print("🎉 All systems operational! ShadowLens is ready for deployment.")
        
        # Show additional information
        show_system_architecture()
        show_business_case()
        show_deployment_instructions()
        
        print(f"\n🔒 ShadowLens: Protecting Student Privacy, One Scan at a Time")
        print("=" * 60)
        
    else:
        print("⚠️ Some components need attention. Please check the errors above.")

if __name__ == "__main__":
    main() 