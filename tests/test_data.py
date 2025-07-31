"""
ShadowLens Test Data
Sample data for testing and development
"""

# Sample EdTech website data for testing
SAMPLE_EDTECH_DATA = {
    "url": "https://example-edtech.com/student-registration",
    "timestamp": "2024-01-15T10:30:00Z",
    "forms": [
        {
            "id": "registration-form",
            "action": "/submit-registration",
            "method": "post",
            "fields": [
                {
                    "type": "text",
                    "name": "student_name",
                    "placeholder": "Enter your full name",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "email",
                    "name": "student_email",
                    "placeholder": "Enter your email address",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "tel",
                    "name": "parent_phone",
                    "placeholder": "Parent's phone number",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "school_name",
                    "placeholder": "Your school name",
                    "required": False,
                    "sensitive": False
                },
                {
                    "type": "number",
                    "name": "student_age",
                    "placeholder": "Your age",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "emergency_contact",
                    "placeholder": "Emergency contact name",
                    "required": True,
                    "sensitive": True
                }
            ]
        }
    ],
    "text": """
    Welcome to ExampleEdTech - The Premier Learning Platform
    
    Our platform is certified by Google for Education and officially partnered with Microsoft.
    We collect personal information to provide personalized learning experiences.
    
    Privacy Policy: We may share your data with third-party partners for analytics and marketing purposes.
    By using our service, you agree to our data collection practices.
    
    Terms of Service: Your information may be used for targeted advertising and research purposes.
    We use cookies and tracking technologies to enhance your experience.
    
    Join thousands of students who trust us with their educational journey!
    """,
    "images": [
        {
            "src": "https://example-edtech.com/images/google-certified.png",
            "alt": "Google Certified for Education",
            "title": "Google Certified",
            "filename": "google-certified.png",
            "brandRelated": True
        },
        {
            "src": "https://example-edtech.com/images/microsoft-partner.png",
            "alt": "Microsoft Official Partner",
            "title": "Microsoft Partner",
            "filename": "microsoft-partner.png",
            "brandRelated": True
        },
        {
            "src": "https://example-edtech.com/images/student-learning.jpg",
            "alt": "Students learning online",
            "title": "Online Learning",
            "filename": "student-learning.jpg",
            "brandRelated": False
        }
    ],
    "meta": {
        "description": "Premier online learning platform certified by Google and Microsoft",
        "keywords": "education, learning, certified, google, microsoft",
        "author": "ExampleEdTech Inc.",
        "robots": "index, follow"
    },
    "riskIndicators": [
        {
            "type": "privacy_term",
            "term": "privacy policy",
            "risk": "medium"
        },
        {
            "type": "privacy_term",
            "term": "data collection",
            "risk": "high"
        },
        {
            "type": "brand_claim",
            "term": "certified by google",
            "risk": "high"
        },
        {
            "type": "brand_claim",
            "term": "microsoft partner",
            "risk": "high"
        },
        {
            "type": "privacy_term",
            "term": "third party",
            "risk": "medium"
        },
        {
            "type": "privacy_term",
            "term": "marketing purposes",
            "risk": "high"
        }
    ]
}

# Sample safe EdTech website data
SAMPLE_SAFE_DATA = {
    "url": "https://safe-learning.org/courses",
    "timestamp": "2024-01-15T10:30:00Z",
    "forms": [
        {
            "id": "course-enrollment",
            "action": "/enroll",
            "method": "post",
            "fields": [
                {
                    "type": "text",
                    "name": "course_name",
                    "placeholder": "Course name",
                    "required": True,
                    "sensitive": False
                },
                {
                    "type": "email",
                    "name": "contact_email",
                    "placeholder": "Contact email",
                    "required": False,
                    "sensitive": True
                }
            ]
        }
    ],
    "text": """
    Welcome to SafeLearning - Your Trusted Educational Resource
    
    We are committed to protecting student privacy and maintaining the highest standards of data security.
    Our platform complies with COPPA and FERPA regulations.
    
    Privacy Policy: We do not collect unnecessary personal information. All data is encrypted and stored securely.
    We do not share personal information with third parties without explicit consent.
    
    Terms of Service: We use minimal cookies for essential functionality only.
    No tracking or advertising technologies are used on our platform.
    
    Join our community of learners in a safe, privacy-focused environment.
    """,
    "images": [
        {
            "src": "https://safe-learning.org/images/logo.png",
            "alt": "SafeLearning Logo",
            "title": "SafeLearning",
            "filename": "logo.png",
            "brandRelated": False
        }
    ],
    "meta": {
        "description": "Privacy-focused online learning platform",
        "keywords": "education, privacy, safe learning",
        "author": "SafeLearning Inc.",
        "robots": "index, follow"
    },
    "riskIndicators": [
        {
            "type": "privacy_term",
            "term": "privacy policy",
            "risk": "low"
        },
        {
            "type": "privacy_term",
            "term": "data security",
            "risk": "low"
        }
    ]
}

# Sample high-risk EdTech website data
SAMPLE_HIGH_RISK_DATA = {
    "url": "https://suspicious-edtech.net/register",
    "timestamp": "2024-01-15T10:30:00Z",
    "forms": [
        {
            "id": "comprehensive-registration",
            "action": "/register",
            "method": "post",
            "fields": [
                {
                    "type": "text",
                    "name": "full_name",
                    "placeholder": "Full legal name",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "email",
                    "name": "email",
                    "placeholder": "Email address",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "tel",
                    "name": "phone",
                    "placeholder": "Phone number",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "address",
                    "placeholder": "Home address",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "ssn",
                    "placeholder": "Social Security Number",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "parent_income",
                    "placeholder": "Parent's annual income",
                    "required": True,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "medical_conditions",
                    "placeholder": "Medical conditions",
                    "required": False,
                    "sensitive": True
                },
                {
                    "type": "text",
                    "name": "credit_card",
                    "placeholder": "Credit card number",
                    "required": True,
                    "sensitive": True
                }
            ]
        }
    ],
    "text": """
    Welcome to SuperLearning - The Ultimate Educational Experience!
    
    We are officially certified by Google, Microsoft, Apple, and Amazon!
    Our platform is trusted by millions of students worldwide.
    
    Privacy Policy: We collect comprehensive personal information to provide the best experience.
    Your data may be shared with our partners for research, marketing, and advertising purposes.
    We use advanced tracking technologies to personalize your experience.
    
    Terms of Service: By using our platform, you agree to share all personal information.
    We may sell your data to third parties for commercial purposes.
    Location tracking is enabled by default for enhanced features.
    
    Join now and get access to exclusive content!
    """,
    "images": [
        {
            "src": "https://suspicious-edtech.net/images/fake-google-cert.png",
            "alt": "Google Certified for Education",
            "title": "Google Certified",
            "filename": "fake-google-cert.png",
            "brandRelated": True
        },
        {
            "src": "https://suspicious-edtech.net/images/fake-microsoft.png",
            "alt": "Microsoft Official Partner",
            "title": "Microsoft Partner",
            "filename": "fake-microsoft.png",
            "brandRelated": True
        },
        {
            "src": "https://suspicious-edtech.net/images/fake-apple.png",
            "alt": "Apple Education Partner",
            "title": "Apple Partner",
            "filename": "fake-apple.png",
            "brandRelated": True
        }
    ],
    "meta": {
        "description": "Ultimate learning platform certified by all major tech companies",
        "keywords": "education, certified, google, microsoft, apple, amazon",
        "author": "SuperLearning Inc.",
        "robots": "index, follow"
    },
    "riskIndicators": [
        {
            "type": "privacy_term",
            "term": "comprehensive personal information",
            "risk": "high"
        },
        {
            "type": "privacy_term",
            "term": "marketing purposes",
            "risk": "high"
        },
        {
            "type": "privacy_term",
            "term": "sell your data",
            "risk": "high"
        },
        {
            "type": "privacy_term",
            "term": "location tracking",
            "risk": "high"
        },
        {
            "type": "brand_claim",
            "term": "certified by google",
            "risk": "high"
        },
        {
            "type": "brand_claim",
            "term": "microsoft official partner",
            "risk": "high"
        },
        {
            "type": "brand_claim",
            "term": "apple education partner",
            "risk": "high"
        }
    ]
}

# Expected analysis results for testing
EXPECTED_ANALYSIS_RESULTS = {
    "safe_site": {
        "summary": "SafeLearning appears to be a privacy-focused educational platform with minimal data collection and clear privacy policies.",
        "risk_score": 2,
        "recommendation": "Safe",
        "red_flags": [],
        "privacy_threats": [],
        "brand_impersonation": [],
        "data_collection_analysis": "Minimal and appropriate data collection practices",
        "student_safety_concerns": []
    },
    "medium_risk_site": {
        "summary": "ExampleEdTech collects significant personal information and makes brand claims that should be verified.",
        "risk_score": 6,
        "recommendation": "Caution",
        "red_flags": [
            "Collects sensitive student information",
            "Makes unverified brand certification claims",
            "Shares data with third parties for marketing"
        ],
        "privacy_threats": [
            "Excessive collection of personal data",
            "Third-party data sharing for marketing"
        ],
        "brand_impersonation": [
            "Claims Google and Microsoft certification without verification"
        ],
        "data_collection_analysis": "Collects extensive personal information including age and emergency contacts",
        "student_safety_concerns": [
            "Potential exposure of student data to third parties"
        ]
    },
    "high_risk_site": {
        "summary": "SuperLearning exhibits multiple serious privacy violations and suspicious brand claims.",
        "risk_score": 9,
        "recommendation": "Dangerous",
        "red_flags": [
            "Requests Social Security Number",
            "Collects credit card information",
            "Makes multiple unverified brand claims",
            "Explicitly states data will be sold"
        ],
        "privacy_threats": [
            "Excessive collection of highly sensitive data",
            "Explicit data selling practices",
            "Location tracking without clear consent"
        ],
        "brand_impersonation": [
            "Multiple unverified certifications from major tech companies",
            "Suspicious brand partnership claims"
        ],
        "data_collection_analysis": "Collects extremely sensitive information including SSN and credit card data",
        "student_safety_concerns": [
            "High risk of identity theft",
            "Potential financial fraud",
            "Excessive data collection from minors"
        ]
    }
}

# Test cases for different scenarios
TEST_CASES = [
    {
        "name": "Safe Educational Platform",
        "data": SAMPLE_SAFE_DATA,
        "expected_risk": "low",
        "expected_score": 1,
        "description": "Minimal data collection, clear privacy policies"
    },
    {
        "name": "Medium Risk Platform",
        "data": SAMPLE_EDTECH_DATA,
        "expected_risk": "medium",
        "expected_score": 6,
        "description": "Some concerning practices, unverified claims"
    },
    {
        "name": "High Risk Platform",
        "data": SAMPLE_HIGH_RISK_DATA,
        "expected_risk": "high",
        "expected_score": 9,
        "description": "Multiple serious violations and suspicious claims"
    }
]

def get_test_data(test_type="medium"):
    """Get test data by type"""
    test_data = {
        "safe": SAMPLE_SAFE_DATA,
        "medium": SAMPLE_EDTECH_DATA,
        "high": SAMPLE_HIGH_RISK_DATA
    }
    return test_data.get(test_type, SAMPLE_EDTECH_DATA)

def get_expected_result(test_type="medium"):
    """Get expected analysis result by type"""
    result_map = {
        "safe": EXPECTED_ANALYSIS_RESULTS["safe_site"],
        "medium": EXPECTED_ANALYSIS_RESULTS["medium_risk_site"],
        "high": EXPECTED_ANALYSIS_RESULTS["high_risk_site"]
    }
    return result_map.get(test_type, EXPECTED_ANALYSIS_RESULTS["medium_risk_site"]) 