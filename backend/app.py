#!/usr/bin/env python3
"""
ShadowLens AI Backend - Enhanced Privacy Analysis
"""

import os
import logging
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import re
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShadowLensAI:
    def __init__(self):
        self.config = type('Config', (), {
            'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', 'AIzaSyCpxYzcgkVPk1X8QiC05Rc6-KNd-np81i8')
        })()
        self.gemini_model = None
        self.init_gemini()
        
        # Enhanced detection patterns
        self.deception_patterns = [
            # Ambiguous language
            r'\b(we may|we might|we could|we can|we reserve the right)\b',
            r'\b(including but not limited to|such as|for example|and others)\b',
            r'\b(reasonable|appropriate|necessary|as needed|when required)\b',
            r'\b(third parties|partners|affiliates|service providers)\b',
            r'\b(improve our services|enhance user experience|provide better features)\b',
            
            # Hidden data collection
            r'\b(background|passive|automatic|continuous|ongoing)\s+(collection|tracking|monitoring)',
            r'\b(device information|usage data|analytics|metrics|statistics)\b',
            r'\b(cookies|pixels|beacons|fingerprinting|tracking)\b',
            
            # Deceptive practices
            r'\b(opt-out|unsubscribe|disable|turn off)\b.*\b(difficult|complicated|multiple steps)',
            r'\b(required|mandatory|essential)\b.*\b(optional|voluntary|your choice)',
            r'\b(we don\'t sell|we don\'t share)\b.*\b(except|however|but)\b',
            
            # FERPA/GDPR compliance issues
            r'\b(student records|educational records|academic information)\b.*\b(without consent|without notice)',
            r'\b(under 13|children|minors)\b.*\b(collect|gather|obtain)\b',
            r'\b(consent|permission)\b.*\b(parental|guardian)\b.*\b(not required|optional)',
            r'\b(educational institution|school|university)\b.*\b(third party|external|commercial)\b'
        ]
        
        self.ferpa_keywords = [
            'student records', 'educational records', 'academic information',
            'grades', 'attendance', 'disciplinary records', 'directory information',
            'personally identifiable information', 'PII', 'student data'
        ]
        
        self.gdpr_keywords = [
            'personal data', 'data subject', 'data controller', 'data processor',
            'right to be forgotten', 'right to access', 'data portability',
            'consent', 'legitimate interest', 'data protection officer',
            'privacy by design', 'data minimization', 'purpose limitation'
        ]
    
    def init_gemini(self):
        """Initialize Gemini AI model with fallback options"""
        try:
            genai.configure(api_key=self.config.GEMINI_API_KEY)
            # Try different model names
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("✅ Gemini 1.5 Pro initialized successfully")
            except:
                try:
                    self.gemini_model = genai.GenerativeModel('gemini-1.0-pro')
                    logger.info("✅ Gemini 1.0 Pro initialized successfully")
                except:
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini Pro initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            self.gemini_model = None
    
    def detect_deception(self, text):
        """Detect deceptive or ambiguous language in privacy policies"""
        deception_indicators = []
        text_lower = text.lower()
        
        for pattern in self.deception_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                deception_indicators.append({
                    'type': 'deceptive_language',
                    'pattern': pattern,
                    'matches': len(matches),
                    'examples': matches[:3]  # Show first 3 examples
                })
        
        return deception_indicators

    def check_ferpa_compliance(self, text):
        """Check for FERPA compliance issues"""
        ferpa_issues = []
        text_lower = text.lower()
        
        # Check for student data collection without proper safeguards
        if any(keyword in text_lower for keyword in self.ferpa_keywords):
            if 'consent' not in text_lower and 'permission' not in text_lower:
                ferpa_issues.append("Student data collection without explicit consent")
            
            if 'third party' in text_lower or 'external' in text_lower:
                ferpa_issues.append("Student data sharing with third parties")
            
            if 'commercial' in text_lower or 'marketing' in text_lower:
                ferpa_issues.append("Commercial use of student data")
        
        return ferpa_issues

    def check_gdpr_compliance(self, text):
        """Check for GDPR compliance issues"""
        gdpr_issues = []
        text_lower = text.lower()
        
        # Check for GDPR requirements
        if 'personal data' in text_lower:
            if 'right to be forgotten' not in text_lower:
                gdpr_issues.append("Missing right to be forgotten")
            
            if 'data portability' not in text_lower:
                gdpr_issues.append("Missing data portability rights")
            
            if 'consent' in text_lower and 'withdraw' not in text_lower:
                gdpr_issues.append("Missing consent withdrawal mechanism")
        
        return gdpr_issues

    def generate_student_summary(self, text):
        """Generate student-friendly summary of privacy policy"""
        if not self.gemini_model:
            return "AI summarization not available"
        
        try:
            prompt = f"""
            Summarize this privacy policy in simple, student-friendly language. 
            Focus on what data is collected, how it's used, and what rights students have.
            Keep it under 200 words and use simple language.
            
            Privacy Policy Text:
            {text[:3000]}
            
            Provide a clear, easy-to-understand summary:
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Unable to generate summary"

    def analyze_with_gemini(self, data):
        """Enhanced AI analysis with deception detection and compliance checking"""
        if not self.gemini_model:
            return self.fallback_analysis(data)
    
        try:
            text = data.get('text', '')
            url = data.get('url', '')
            website_type = data.get('websiteType', 'general')
            is_legal_document = data.get('isLegalDocument', False)
            document_type = data.get('documentType', '')
            
            # Enhanced prompt for comprehensive analysis
            prompt = f"""
            Analyze this website's privacy practices and provide a comprehensive assessment.
            
            Website: {url}
            Type: {website_type}
            Document Type: {document_type}
            Content: {text[:5000]}
            
            Provide analysis in JSON format with:
            1. risk_score (0-10)
            2. recommendation (Safe/Moderate/High Risk/Dangerous)
            3. privacy_threats (list of specific threats)
            4. deception_indicators (ambiguous or deceptive practices)
            5. ferpa_compliance (FERPA compliance issues)
            6. gdpr_compliance (GDPR compliance issues)
            7. student_summary (simple explanation for students)
            8. red_flags (critical issues)
            9. brand_impersonation (fake brand indicators)
            10. summary (overall assessment)
            
            Focus on educational privacy, student data protection, and deceptive practices.
            """
            
            response = self.gemini_model.generate_content(prompt)
            
        try:
                # Try to parse JSON response
                result = json.loads(response.text)
                return result
            except:
                # If JSON parsing fails, extract key information
                return self.extract_ai_analysis(response.text, data)
                
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return self.fallback_analysis(data)
    
    def extract_ai_analysis(self, ai_text, data):
        """Extract analysis from AI text response"""
        # Extract risk score
        risk_score = 5  # Default
        if 'risk_score' in ai_text.lower():
            try:
                score_match = re.search(r'risk_score[:\s]*(\d+)', ai_text.lower())
            if score_match:
                risk_score = int(score_match.group(1))
            except:
                pass
        
        # Extract recommendation
        recommendation = "Moderate"
        if 'dangerous' in ai_text.lower():
            recommendation = "Dangerous"
        elif 'high risk' in ai_text.lower():
            recommendation = "High Risk"
        elif 'safe' in ai_text.lower():
            recommendation = "Safe"
        
        return {
            'risk_score': risk_score,
            'recommendation': recommendation,
            'privacy_threats': self.extract_threats(ai_text),
            'deception_indicators': self.detect_deception(data.get('text', '')),
            'ferpa_compliance': self.check_ferpa_compliance(data.get('text', '')),
            'gdpr_compliance': self.check_gdpr_compliance(data.get('text', '')),
            'student_summary': self.generate_student_summary(data.get('text', '')),
            'red_flags': self.extract_red_flags(ai_text),
            'brand_impersonation': [],
            'summary': ai_text[:200] + "..." if len(ai_text) > 200 else ai_text,
            'ai_model': 'gemini-enhanced'
        }

    def extract_threats(self, text):
        """Extract privacy threats from AI response"""
        threats = []
        threat_keywords = [
            'data collection', 'tracking', 'cookies', 'third party',
            'marketing', 'advertising', 'analytics', 'personal information'
        ]
        
        for keyword in threat_keywords:
            if keyword in text.lower():
                threats.append(f"Privacy term found: {keyword}")
        
        return threats

    def extract_red_flags(self, text):
        """Extract red flags from AI response"""
        red_flags = []
        if 'student' in text.lower() and 'data' in text.lower():
            red_flags.append("Student data collection detected")
        if 'third party' in text.lower():
            red_flags.append("Third-party data sharing")
        if 'marketing' in text.lower():
            red_flags.append("Marketing use of data")
        
        return red_flags
    
    def fallback_analysis(self, data):
        """Enhanced fallback analysis with all features"""
        text = data.get('text', '').lower()
        url = data.get('url', '').lower()
        website_type = data.get('websiteType', 'general')
        is_legal_document = data.get('isLegalDocument', False)
        document_type = data.get('documentType', '')
        
        # Base risk score calculation
        base_risk = 2
        
        # Website type adjustments
        if 'social_media' in website_type:
            base_risk += 3
        elif 'financial' in website_type:
            base_risk += 2
        elif 'educational' in website_type:
            base_risk += 1
        
        # Legal document analysis
        if is_legal_document:
            base_risk += 2
            if 'privacy_policy' in document_type:
                base_risk += 1
            elif 'terms_of_service' in document_type:
                base_risk += 1
        
        # Enhanced threat detection
        privacy_threats = []
        if 'cookies' in text:
            privacy_threats.append("Privacy term found: cookies")
        if 'tracking' in text:
            privacy_threats.append("Privacy term found: tracking")
        if 'marketing' in text:
            privacy_threats.append("Privacy term found: marketing")
        if 'third party' in text:
            privacy_threats.append("Privacy term found: third party")
        if 'analytics' in text:
            privacy_threats.append("Privacy term found: analytics")
        
        # Deception detection
        deception_indicators = self.detect_deception(data.get('text', ''))
        
        # Compliance checking
        ferpa_issues = self.check_ferpa_compliance(data.get('text', ''))
        gdpr_issues = self.check_gdpr_compliance(data.get('text', ''))
        
        # Risk score calculation
        risk_score = min(10, base_risk + len(privacy_threats) + len(deception_indicators) + len(ferpa_issues) + len(gdpr_issues))
        
        # Recommendation based on risk score
        if risk_score >= 8:
            recommendation = "Dangerous"
        elif risk_score >= 6:
            recommendation = "High Risk"
        elif risk_score >= 4:
            recommendation = "Caution"
        elif risk_score >= 2:
            recommendation = "Moderate"
        else:
            recommendation = "Safe"
        
        # Student summary
        student_summary = self.generate_student_summary(data.get('text', ''))
        
        return {
            'risk_score': risk_score,
            'recommendation': recommendation,
            'privacy_threats': privacy_threats,
            'deception_indicators': deception_indicators,
            'ferpa_compliance': ferpa_issues,
            'gdpr_compliance': gdpr_issues,
            'student_summary': student_summary,
            'red_flags': [f"{website_type} platform detected - data collection risk"] if website_type != 'general' else [],
            'brand_impersonation': [],
            'summary': f"Analysis of {website_type} website with {len(privacy_threats)} privacy threats detected",
            'ai_model': 'enhanced-fallback'
        }

# Initialize AI
ai_analyzer = ShadowLensAI()

# Flask app
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_model': 'gemini-enhanced' if ai_analyzer.gemini_model else 'fallback',
        'features': [
            'AI Summarization',
            'Deception Detection', 
            'FERPA/GDPR Compliance',
            'Risk Scoring',
            'Real-time Analysis'
        ]
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Enhanced analysis endpoint with all features"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Perform enhanced analysis
        result = ai_analyzer.analyze_with_gemini(data)
        
        # Add metadata
        result['features_used'] = [
            'AI Summarization',
            'Deception Detection',
            'FERPA/GDPR Compliance Checking',
            'Enhanced Risk Scoring',
            'Student-Friendly Summary'
        ]
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    """Generate student-friendly summary"""
    try:
        data = request.json
        text = data.get('text', '')
        
        summary = ai_analyzer.generate_student_summary(text)
        
        return jsonify({
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary)
        })
        
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/detect-deception', methods=['POST'])
def detect_deception():
    """Detect deceptive practices"""
    try:
        data = request.json
        text = data.get('text', '')
        
        deception_indicators = ai_analyzer.detect_deception(text)
        
        return jsonify({
            'deception_indicators': deception_indicators,
            'total_indicators': len(deception_indicators)
        })
        
    except Exception as e:
        logger.error(f"Deception detection error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/compliance-check', methods=['POST'])
def compliance_check():
    """Check FERPA and GDPR compliance"""
    try:
        data = request.json
        text = data.get('text', '')
        
        ferpa_issues = ai_analyzer.check_ferpa_compliance(text)
        gdpr_issues = ai_analyzer.check_gdpr_compliance(text)
        
    return jsonify({
            'ferpa_compliance': ferpa_issues,
            'gdpr_compliance': gdpr_issues,
            'ferpa_issues_count': len(ferpa_issues),
            'gdpr_issues_count': len(gdpr_issues)
        })
        
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting ShadowLens AI Backend on port 5000")
    logger.info("🤖 AI Model: Gemini Pro")
    app.run(host='0.0.0.0', port=5000, debug=False) 