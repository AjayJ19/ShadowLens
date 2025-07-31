#!/usr/bin/env python3
"""
ShadowLens Demo Script
Demonstrates the AI-powered privacy analysis system
"""

import requests
import json
import time
from tests.test_data import get_test_data, get_expected_result

def demo_analysis():
    """Demonstrate ShadowLens analysis capabilities"""
    
    print("🔒 ShadowLens Demo")
    print("=" * 50)
    
    # Test different scenarios
    test_cases = [
        ("Safe EdTech Site", "safe"),
        ("Medium Risk Site", "medium"), 
        ("High Risk Site", "high")
    ]
    
    for name, test_type in test_cases:
        print(f"\n📊 Testing: {name}")
        print("-" * 30)
        
        # Get test data
        data = get_test_data(test_type)
        
        try:
            # Send to backend
            response = requests.post(
                'http://localhost:5000/analyze',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Analysis Complete")
                print(f"   URL: {result.get('url', 'Unknown')}")
                print(f"   Risk Score: {result.get('risk_score', 0)}/10")
                print(f"   Recommendation: {result.get('recommendation', 'Unknown')}")
                print(f"   AI Model: {result.get('ai_model', 'Unknown')}")
                
                if result.get('red_flags'):
                    print(f"   Red Flags: {len(result['red_flags'])} found")
                    for flag in result['red_flags'][:3]:  # Show first 3
                        print(f"     • {flag}")
                
                if result.get('privacy_threats'):
                    print(f"   Privacy Threats: {len(result['privacy_threats'])} found")
                
                if result.get('brand_impersonation'):
                    print(f"   Brand Impersonation: {len(result['brand_impersonation'])} found")
                
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Backend not running. Please start the backend first.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        time.sleep(1)
    
    return True

def demo_api_endpoints():
    """Demonstrate available API endpoints"""
    
    print(f"\n🌐 API Endpoints Demo")
    print("=" * 30)
    
    endpoints = [
        ("Health Check", "GET", "/health"),
        ("Configuration", "GET", "/config"),
    ]
    
    for name, method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:5000{endpoint}")
            else:
                response = requests.post(f"http://localhost:5000{endpoint}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {name}: {endpoint}")
                print(f"   Status: {response.status_code}")
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"   {key}: {value}")
            else:
                print(f"❌ {name}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Backend not running")
        except Exception as e:
            print(f"❌ {name}: {e}")
        
        print()

def demo_chrome_extension():
    """Demonstrate Chrome extension features"""
    
    print(f"\n🔧 Chrome Extension Demo")
    print("=" * 30)
    
    features = [
        "Real-time privacy threat detection",
        "Form field analysis (sensitive data collection)",
        "Brand impersonation detection",
        "Risk scoring (1-10 scale)",
        "Consent banner for user privacy",
        "Popup dashboard with scan history",
        "Offline analysis capability",
        "Export functionality for compliance reporting"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i:2d}. {feature}")
    
    print(f"\n📁 Extension Location: chrome-extension/")
    print(f"📋 To load in Chrome:")
    print(f"   1. Open Chrome")
    print(f"   2. Go to chrome://extensions/")
    print(f"   3. Enable 'Developer mode'")
    print(f"   4. Click 'Load unpacked'")
    print(f"   5. Select the chrome-extension/ folder")

def demo_business_case():
    """Demonstrate business potential"""
    
    print(f"\n💰 Business Case Demo")
    print("=" * 30)
    
    metrics = [
        ("Global EdTech Market", "$123B (2022)", "13.6% CAGR"),
        ("K-12 Students (US)", "50.8M", "Growing"),
        ("Privacy Protection Market", "$2.1B", "25% CAGR"),
        ("Target Addressable Market", "$15B", "Multiple segments"),
    ]
    
    print("📊 Market Opportunity:")
    for metric, value, growth in metrics:
        print(f"   {metric}: {value} ({growth})")
    
    revenue_models = [
        ("B2B SaaS - School Districts", "$5-10/student/year", "$350M potential"),
        ("B2C Premium - Parent App", "$2.99/month", "$180M potential"),
        ("API Certification Service", "$0.01/scan", "$50M potential"),
        ("NGO/Research Editions", "Grant-funded", "Social impact"),
    ]
    
    print(f"\n💼 Revenue Models:")
    for model, pricing, potential in revenue_models:
        print(f"   {model}")
        print(f"     Pricing: {pricing}")
        print(f"     Potential: {potential}")

def main():
    """Run the complete demo"""
    
    print("🚀 ShadowLens - AI-Powered Privacy Guardian for EdTech")
    print("=" * 60)
    print()
    
    # Check if backend is running
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Please start it first:")
        print("   cd backend && python app.py")
        return
    
    # Run demos
    if demo_analysis():
        demo_api_endpoints()
        demo_chrome_extension()
        demo_business_case()
        
        print(f"\n🎉 Demo Complete!")
        print("=" * 30)
        print("Next steps:")
        print("1. Load Chrome extension from chrome-extension/")
        print("2. Visit EdTech sites to see real-time scanning")
        print("3. Check the popup dashboard for results")
        print("4. Explore the business dashboard at http://localhost:3000")
        print()
        print("🔒 ShadowLens: Protecting Student Privacy, One Scan at a Time")

if __name__ == "__main__":
    main() 