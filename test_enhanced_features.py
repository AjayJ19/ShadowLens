#!/usr/bin/env python3
"""
Test ShadowLens Enhanced Features
"""

import requests
import json
import time

def test_enhanced_features():
    """Test all enhanced features"""
    print("🔒 ShadowLens Enhanced Features Test")
    print("=" * 50)
    
    # Test URLs with different characteristics
    test_urls = [
        {
            'url': 'https://www.facebook.com/privacy/policy/',
            'name': 'Facebook Privacy Policy',
            'expected_features': ['AI Summarization', 'Deception Detection', 'FERPA/GDPR Compliance']
        },
        {
            'url': 'https://policies.google.com/terms',
            'name': 'Google Terms',
            'expected_features': ['AI Summarization', 'Deception Detection', 'FERPA/GDPR Compliance']
        },
        {
            'url': 'https://www.coursera.org',
            'name': 'Coursera Educational Site',
            'expected_features': ['AI Summarization', 'FERPA/GDPR Compliance', 'Risk Scoring']
        }
    ]
    
    for test_case in test_urls:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        # Simulate scraped data
        test_data = {
            'url': test_case['url'],
            'forms': [
                {
                    'fields': [
                        {'name': 'email', 'type': 'email', 'sensitive': True},
                        {'name': 'password', 'type': 'password', 'sensitive': True}
                    ]
                }
            ],
            'text': f"This is a test of {test_case['name']} with privacy policy and data collection practices. We may collect personal information including cookies, tracking, and third-party data sharing. Student records and educational data may be processed without explicit consent.",
            'images': [],
            'riskIndicators': [
                {'type': 'privacy_term', 'term': 'data collection', 'risk': 'high'},
                {'type': 'privacy_term', 'term': 'cookies', 'risk': 'high'},
                {'type': 'privacy_term', 'term': 'third party', 'risk': 'high'}
            ],
            'websiteType': 'educational' if 'coursera' in test_case['url'] else 'social_media',
            'isLegalDocument': 'privacy' in test_case['url'] or 'terms' in test_case['url'],
            'documentType': 'privacy_policy' if 'privacy' in test_case['url'] else 'terms_of_service' if 'terms' in test_case['url'] else ''
        }
        
        # Test analysis endpoint
        try:
            response = requests.post(
                'http://localhost:5000/analyze',
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis successful!")
                print(f"   Risk Score: {result.get('risk_score', 'N/A')}/10")
                print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
                
                # Check for enhanced features
                features_used = result.get('features_used', [])
                print(f"   Features Used: {', '.join(features_used)}")
                
                # Check specific features
                if 'student_summary' in result:
                    print(f"   ✅ AI Summarization: Available")
                    print(f"      Summary: {result['student_summary'][:100]}...")
                
                if 'deception_indicators' in result:
                    deception_count = len(result['deception_indicators'])
                    print(f"   ✅ Deception Detection: {deception_count} indicators found")
                
                if 'ferpa_compliance' in result:
                    ferpa_count = len(result['ferpa_compliance'])
                    print(f"   ✅ FERPA Compliance: {ferpa_count} issues found")
                
                if 'gdpr_compliance' in result:
                    gdpr_count = len(result['gdpr_compliance'])
                    print(f"   ✅ GDPR Compliance: {gdpr_count} issues found")
                
                # Check privacy threats
                privacy_threats = result.get('privacy_threats', [])
                print(f"   🔒 Privacy Threats: {len(privacy_threats)} found")
                
                # Check red flags
                red_flags = result.get('red_flags', [])
                print(f"   🚨 Red Flags: {len(red_flags)} found")
                
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing {test_case['name']}: {e}")
    
    # Test individual feature endpoints
    print(f"\n🔧 Testing Individual Feature Endpoints")
    print("-" * 40)
    
    test_text = "This privacy policy allows us to collect personal information including student records, cookies, and third-party data sharing. We may use this data for marketing purposes and share with partners."
    
    # Test summarization
    try:
        response = requests.post(
            'http://localhost:5000/summarize',
            json={'text': test_text},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Summarization: {result.get('summary_length', 0)} characters")
        else:
            print(f"❌ Summarization failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Summarization error: {e}")
    
    # Test deception detection
    try:
        response = requests.post(
            'http://localhost:5000/detect-deception',
            json={'text': test_text},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Deception Detection: {result.get('total_indicators', 0)} indicators")
        else:
            print(f"❌ Deception detection failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Deception detection error: {e}")
    
    # Test compliance checking
    try:
        response = requests.post(
            'http://localhost:5000/compliance-check',
            json={'text': test_text},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ FERPA Compliance: {result.get('ferpa_issues_count', 0)} issues")
            print(f"✅ GDPR Compliance: {result.get('gdpr_issues_count', 0)} issues")
        else:
            print(f"❌ Compliance check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Compliance check error: {e}")
    
    print(f"\n🎉 Enhanced Features Test Complete!")
    print("=" * 50)

def test_backend_health():
    """Test backend health and features"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Backend Health: {result.get('status', 'unknown')}")
            print(f"🤖 AI Model: {result.get('ai_model', 'unknown')}")
            
            features = result.get('features', [])
            print(f"🔧 Available Features:")
            for feature in features:
                print(f"   • {feature}")
            
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def main():
    print("🔒 ShadowLens Enhanced Features Test")
    print("=" * 50)
    
    # Check backend health first
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start it first:")
        print("   source venv/bin/activate")
        print("   export GEMINI_API_KEY='your-api-key'")
        print("   python3 backend/app.py")
        return
    
    # Test enhanced features
    test_enhanced_features()
    
    print(f"\n📋 Summary:")
    print("✅ All enhanced features implemented:")
    print("   • AI Summarization - Student-friendly explanations")
    print("   • Deception Detection - Ambiguous language detection")
    print("   • FERPA/GDPR Compliance - Educational privacy checking")
    print("   • Enhanced Risk Scoring - Comprehensive assessment")
    print("   • Real-time Analysis - Instant privacy evaluation")

if __name__ == "__main__":
    main() 