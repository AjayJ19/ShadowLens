#!/usr/bin/env python3
"""
ShadowLens System Test
Tests all components of the system
"""

import requests
import json
import time
from tests.test_data import get_test_data, get_expected_result

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running")
        return False

def test_analysis_endpoint():
    """Test analysis endpoint with sample data"""
    try:
        test_data = get_test_data("medium")
        response = requests.post(
            'http://localhost:5000/analyze',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis endpoint working")
            print(f"   Risk Score: {result.get('risk_score', 'N/A')}/10")
            print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
            return True
        else:
            print(f"❌ Analysis endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running")
        return False

def test_dashboard():
    """Test dashboard accessibility"""
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Dashboard accessible")
            return True
        else:
            print("❌ Dashboard not accessible")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard not running")
        return False

def main():
    """Run all tests"""
    print("🔒 ShadowLens System Test")
    print("========================")
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Analysis Endpoint", test_analysis_endpoint),
        ("Dashboard", test_dashboard)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! ShadowLens is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the setup.")

if __name__ == "__main__":
    main()
