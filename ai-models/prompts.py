"""
ShadowLens AI Prompt Templates
Structured prompts for privacy threat analysis
"""

class PromptTemplates:
    """AI prompt templates for different analysis scenarios"""
    
    @staticmethod
    def gemini_analysis_prompt(data):
        """Main analysis prompt for Gemini Pro"""
        return f"""
You are ShadowLens, an AI privacy guardian for EdTech platforms. Your mission is to protect students by detecting privacy threats, brand impersonation, and risky data collection practices.

ANALYZE THIS WEBSITE DATA:

WEBSITE INFORMATION:
- URL: {data.get('url', 'Unknown')}
- Forms Detected: {len(data.get('forms', []))}
- Sensitive Fields: {PromptTemplates._count_sensitive_fields(data.get('forms', []))}
- Text Content Length: {len(data.get('text', ''))} characters
- Images Analyzed: {len(data.get('images', []))}
- Risk Indicators Found: {len(data.get('riskIndicators', []))}

FORM ANALYSIS:
{PromptTemplates._format_forms(data.get('forms', []))}

TEXT CONTENT (First 1000 characters):
{data.get('text', '')[:1000]}

RISK INDICATORS DETECTED:
{PromptTemplates._format_risk_indicators(data.get('riskIndicators', []))}

IMAGE ANALYSIS:
{PromptTemplates._format_images(data.get('images', []))}

ANALYSIS REQUIREMENTS:

1. PRIVACY THREAT ASSESSMENT:
   - Identify excessive data collection practices
   - Detect vague or misleading privacy terms
   - Assess data sharing and third-party access
   - Evaluate consent mechanisms

2. BRAND IMPERSONATION DETECTION:
   - Identify fake logos or unauthorized brand claims
   - Detect misleading "certified by" or "official partner" claims
   - Assess visual and textual brand associations
   - Flag suspicious trust indicators

3. DATA COLLECTION ANALYSIS:
   - Evaluate the necessity of collected data
   - Assess data retention policies
   - Identify potential data misuse risks
   - Check for age-appropriate data handling

4. RISK SCORING (1-10):
   - 1-3: Safe - Minimal privacy risks
   - 4-6: Caution - Some concerning practices
   - 7-10: Dangerous - Significant privacy threats

5. RECOMMENDATION:
   - Safe: Proceed with normal caution
   - Caution: Be careful with personal data
   - Dangerous: Avoid sharing sensitive information

RESPONSE FORMAT (JSON):
{{
    "summary": "Brief analysis summary (2-3 sentences)",
    "risk_score": <1-10>,
    "recommendation": "Safe|Caution|Dangerous",
    "red_flags": [
        "Specific red flag 1",
        "Specific red flag 2",
        "Specific red flag 3"
    ],
    "privacy_threats": [
        "Detailed privacy threat 1",
        "Detailed privacy threat 2"
    ],
    "brand_impersonation": [
        "Brand impersonation issue 1",
        "Brand impersonation issue 2"
    ],
    "data_collection_analysis": "Detailed analysis of data collection practices",
    "student_safety_concerns": [
        "Student safety concern 1",
        "Student safety concern 2"
    ]
}}

IMPORTANT: Focus on student privacy and safety. Be thorough but concise. Ensure all JSON fields are properly formatted.
"""

    @staticmethod
    def mistral_analysis_prompt(data):
        """Main analysis prompt for Mistral model"""
        return f"""<s>[INST] You are ShadowLens, an AI privacy guardian for EdTech platforms. Your mission is to protect students by detecting privacy threats, brand impersonation, and risky data collection practices.

ANALYZE THIS WEBSITE DATA:

WEBSITE INFORMATION:
- URL: {data.get('url', 'Unknown')}
- Forms Detected: {len(data.get('forms', []))}
- Sensitive Fields: {PromptTemplates._count_sensitive_fields(data.get('forms', []))}
- Text Content Length: {len(data.get('text', ''))} characters
- Images Analyzed: {len(data.get('images', []))}
- Risk Indicators Found: {len(data.get('riskIndicators', []))}

FORM ANALYSIS:
{PromptTemplates._format_forms(data.get('forms', []))}

TEXT CONTENT (First 1000 characters):
{data.get('text', '')[:1000]}

RISK INDICATORS DETECTED:
{PromptTemplates._format_risk_indicators(data.get('riskIndicators', []))}

IMAGE ANALYSIS:
{PromptTemplates._format_images(data.get('images', []))}

ANALYSIS REQUIREMENTS:

1. PRIVACY THREAT ASSESSMENT:
   - Identify excessive data collection practices
   - Detect vague or misleading privacy terms
   - Assess data sharing and third-party access
   - Evaluate consent mechanisms

2. BRAND IMPERSONATION DETECTION:
   - Identify fake logos or unauthorized brand claims
   - Detect misleading "certified by" or "official partner" claims
   - Assess visual and textual brand associations
   - Flag suspicious trust indicators

3. DATA COLLECTION ANALYSIS:
   - Evaluate the necessity of collected data
   - Assess data retention policies
   - Identify potential data misuse risks
   - Check for age-appropriate data handling

4. RISK SCORING (1-10):
   - 1-3: Safe - Minimal privacy risks
   - 4-6: Caution - Some concerning practices
   - 7-10: Dangerous - Significant privacy threats

5. RECOMMENDATION:
   - Safe: Proceed with normal caution
   - Caution: Be careful with personal data
   - Dangerous: Avoid sharing sensitive information

RESPONSE FORMAT (JSON):
{{
    "summary": "Brief analysis summary (2-3 sentences)",
    "risk_score": <1-10>,
    "recommendation": "Safe|Caution|Dangerous",
    "red_flags": [
        "Specific red flag 1",
        "Specific red flag 2",
        "Specific red flag 3"
    ],
    "privacy_threats": [
        "Detailed privacy threat 1",
        "Detailed privacy threat 2"
    ],
    "brand_impersonation": [
        "Brand impersonation issue 1",
        "Brand impersonation issue 2"
    ],
    "data_collection_analysis": "Detailed analysis of data collection practices",
    "student_safety_concerns": [
        "Student safety concern 1",
        "Student safety concern 2"
    ]
}}

IMPORTANT: Focus on student privacy and safety. Be thorough but concise. Ensure all JSON fields are properly formatted. [/INST]</s>"""

    @staticmethod
    def quick_assessment_prompt(data):
        """Quick assessment for real-time analysis"""
        return f"""
QUICK PRIVACY ASSESSMENT:

Website: {data.get('url', 'Unknown')}
Forms: {len(data.get('forms', []))}
Sensitive Fields: {PromptTemplates._count_sensitive_fields(data.get('forms', []))}
Risk Indicators: {len(data.get('riskIndicators', []))}

Provide a quick risk assessment (1-10) and recommendation (Safe/Caution/Dangerous) with 2-3 key red flags.

JSON Response:
{{
    "risk_score": <1-10>,
    "recommendation": "Safe|Caution|Dangerous",
    "red_flags": ["flag1", "flag2", "flag3"],
    "summary": "Quick assessment summary"
}}
"""

    @staticmethod
    def detailed_analysis_prompt(data):
        """Detailed analysis for comprehensive reports"""
        return f"""
COMPREHENSIVE PRIVACY ANALYSIS:

WEBSITE: {data.get('url', 'Unknown')}

DATA COLLECTION:
- Forms: {len(data.get('forms', []))}
- Sensitive Fields: {PromptTemplates._count_sensitive_fields(data.get('forms', []))}
- Text Analysis: {len(data.get('text', ''))} characters
- Images: {len(data.get('images', []))}
- Risk Indicators: {len(data.get('riskIndicators', []))}

DETAILED ANALYSIS REQUIREMENTS:

1. PRIVACY COMPLIANCE:
   - COPPA compliance assessment
   - GDPR/FERPA considerations
   - Age-appropriate data handling
   - Parental consent mechanisms

2. DATA SECURITY:
   - Data transmission security
   - Storage practices
   - Access controls
   - Data retention policies

3. THIRD-PARTY RISKS:
   - Third-party integrations
   - Data sharing practices
   - Advertising and tracking
   - Analytics usage

4. STUDENT SAFETY:
   - Age-appropriate content
   - Social features risks
   - Communication safeguards
   - Location data handling

5. BRAND TRUST:
   - Legitimate partnerships
   - Certification claims
   - Visual trust indicators
   - Reputation assessment

PROVIDE DETAILED JSON RESPONSE:
{{
    "comprehensive_analysis": {{
        "privacy_compliance": "Detailed compliance assessment",
        "data_security": "Security analysis",
        "third_party_risks": "Third-party risk assessment",
        "student_safety": "Safety analysis",
        "brand_trust": "Trust assessment"
    }},
    "risk_score": <1-10>,
    "recommendation": "Safe|Caution|Dangerous",
    "red_flags": ["Detailed flag 1", "Detailed flag 2", "Detailed flag 3"],
    "compliance_issues": ["Compliance issue 1", "Compliance issue 2"],
    "security_concerns": ["Security concern 1", "Security concern 2"],
    "safety_recommendations": ["Safety recommendation 1", "Safety recommendation 2"],
    "summary": "Comprehensive analysis summary"
}}
"""

    # Helper methods for formatting data
    @staticmethod
    def _count_sensitive_fields(forms):
        """Count sensitive fields across all forms"""
        count = 0
        for form in forms:
            for field in form.get('fields', []):
                if field.get('sensitive', False):
                    count += 1
        return count

    @staticmethod
    def _format_forms(forms):
        """Format forms for prompt"""
        if not forms:
            return "No forms detected"
        
        formatted = []
        for i, form in enumerate(forms):
            fields = []
            for field in form.get('fields', []):
                field_info = f"{field.get('type', 'unknown')}: {field.get('name', 'unnamed')}"
                if field.get('sensitive'):
                    field_info += " (SENSITIVE)"
                if field.get('required'):
                    field_info += " (REQUIRED)"
                fields.append(field_info)
            
            formatted.append(f"Form {i+1}: {', '.join(fields)}")
        
        return "\n".join(formatted)

    @staticmethod
    def _format_risk_indicators(indicators):
        """Format risk indicators for prompt"""
        if not indicators:
            return "No risk indicators detected"
        
        formatted = []
        for indicator in indicators:
            formatted.append(f"- {indicator.get('type', 'unknown')}: {indicator.get('term', 'unknown')} ({indicator.get('risk', 'unknown')} risk)")
        
        return "\n".join(formatted)

    @staticmethod
    def _format_images(images):
        """Format image analysis for prompt"""
        if not images:
            return "No images analyzed"
        
        brand_related = [img for img in images if img.get('brandRelated', False)]
        
        formatted = []
        formatted.append(f"Total Images: {len(images)}")
        if brand_related:
            formatted.append(f"Brand-Related Images: {len(brand_related)}")
            for img in brand_related[:3]:  # Show first 3
                formatted.append(f"  - {img.get('alt', 'No alt text')} ({img.get('filename', 'Unknown')})")
        
        return "\n".join(formatted)

    @staticmethod
    def get_prompt_by_type(prompt_type, data):
        """Get prompt by type"""
        prompts = {
            'gemini': PromptTemplates.gemini_analysis_prompt,
            'mistral': PromptTemplates.mistral_analysis_prompt,
            'quick': PromptTemplates.quick_assessment_prompt,
            'detailed': PromptTemplates.detailed_analysis_prompt
        }
        
        if prompt_type not in prompts:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        return prompts[prompt_type](data) 