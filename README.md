# 🔒 ShadowLens - Privacy Guardian for Educational Websites

**Real-time webscraping and privacy analysis for educational platforms**

## 🌟 Features

### 🔍 **Comprehensive Website Analysis**
- **Legal Document Detection**: Automatically detects and analyzes privacy policies, terms of service, and cookie policies
- **Real-time Scraping**: Uses both basic requests and Selenium for JavaScript-heavy sites
- **Multi-method Analysis**: Combines rule-based and AI-powered analysis for accurate results

### 📊 **Dashboard & Analytics**
- **Real-time Tracking**: Monitor all websites analyzed while the extension is active
- **Risk Level Filtering**: Filter websites by risk level (Safe, Moderate, Caution, Dangerous)
- **Search Functionality**: Search through website history by URL or content
- **Analytics Charts**: Visual representation of risk distribution and privacy threats
- **Data Export**: Export analysis history as JSON for further analysis

### 📊 **Detailed Risk Assessment**
- **Risk Scoring**: 1-10 scale with specific recommendations
- **Categorized Threats**: Privacy terms, legal clauses, data sharing, payment collection
- **Website Type Detection**: Educational, social media, financial, e-commerce, government sites

### 🎯 **Specialized Legal Document Analysis**
- **Privacy Policy Analysis**: Detects data collection practices and user rights
- **Terms of Service Review**: Identifies concerning legal clauses and user obligations
- **Cookie Policy Assessment**: Analyzes tracking and data sharing practices

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+ required
python3 --version

# Install dependencies
pip install requests beautifulsoup4 selenium webdriver-manager flask flask-cors google-generativeai transformers torch
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/shadowlens.git
cd shadowlens

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

#### 1. Start the Backend Server
```bash
# Set your Gemini API key (optional, falls back to rule-based analysis)
export GEMINI_API_KEY="your_api_key_here"

# Start the backend server
python3 backend/app.py
```

#### 2. Run Website Analysis
```bash
# In a new terminal
python3 test_any_website.py
```

#### 3. Enter Website URL
When prompted, enter any website URL to analyze:
- **Privacy Policies**: `https://www.facebook.com/privacy/policy/`
- **Terms of Service**: `https://www.amazon.com/gp/help/customer/display.html?nodeId=508088`
- **Educational Sites**: `https://coursera.org`, `https://edx.org`
- **Any other website** you want to analyze

#### 4. View Dashboard (Optional)
```bash
# Start the dashboard server
python3 dashboard/server.py

# Open http://localhost:8080 in your browser
# Watch real-time website analysis history!
```

## 📋 Example Output

```
🔒 ShadowLens - Test Any Educational Website
============================================================

🌐 Enter educational website URL: https://www.facebook.com/privacy/policy/

📋 Detected legal document URL - using specialized analysis...
✅ Legal Document Analysis Complete!
   📄 Document type: privacy_policy
   📝 Text length: 15000 characters
   ⚠️ Risk indicators: 8

⚠️ DETAILED RISK INDICATORS FOUND:
----------------------------------------

🔒 PRIVACY & DATA COLLECTION TERMS (7):
   • cookies - Tracks your browsing behavior
   • marketing - Uses your data for advertising
   • analytics - Monitors your usage patterns
   • user data - Collects your personal information
   • profile - Creates detailed user profiles

⚖️ CONCERNING LEGAL TERMS (1):
   • jurisdiction

🤖 AI Analysis:
   • Risk Score: 10/10
   • Recommendation: Dangerous
   🔴 DANGEROUS: This site has critical privacy concerns!
```

## 🏗️ Architecture

### Core Components

#### 1. **Website Scraper** (`test_any_website.py`)
- **Multi-method Scraping**: Basic requests + Selenium for JavaScript sites
- **Legal Document Detection**: Specialized analysis for privacy policies and terms
- **Content Extraction**: Forms, text, images, and risk indicators

#### 2. **AI Backend** (`backend/app.py`)
- **Gemini Pro Integration**: AI-powered analysis (optional)
- **Rule-based Fallback**: Comprehensive analysis when AI unavailable
- **Risk Assessment**: Multi-factor scoring system

#### 3. **Risk Analysis Engine**
- **Privacy Terms**: Data collection, tracking, marketing practices
- **Legal Clauses**: Concerning terms, user rights, liability limitations
- **Data Sharing**: Third-party sharing, data brokers, advertising partners
- **Payment Collection**: Financial data, credit card information

#### 4. **Dashboard System** (`dashboard/`)
- **Real-time Tracking**: Chrome storage integration for website history
- **Modern UI**: Responsive design with gradient backgrounds and animations
- **Analytics Charts**: Risk distribution and threat analysis visualization
- **Data Management**: Export functionality and search capabilities

### Risk Categories

#### 🔒 **Privacy & Data Collection**
- Cookies and tracking
- Marketing and advertising
- Analytics and monitoring
- Personal data collection
- User profiling

#### ⚖️ **Concerning Legal Terms**
- Liability disclaimers
- Arbitration clauses
- Broad rights grants
- Termination clauses
- Jurisdiction limitations

#### 📤 **Data Sharing Practices**
- Third-party sharing
- Data broker sales
- Advertising partnerships
- Cross-site tracking
- International transfers

## 🎯 Use Cases

### Educational Institutions
- **Course Platform Analysis**: Evaluate privacy practices of online learning platforms
- **Student Data Protection**: Assess how student information is handled
- **Compliance Checking**: Verify GDPR, COPPA, and other privacy regulations

### Privacy Researchers
- **Policy Comparison**: Compare privacy policies across different platforms
- **Trend Analysis**: Track changes in data collection practices
- **Risk Assessment**: Identify concerning patterns in legal documents

### General Users
- **Website Safety**: Check if a website has good privacy practices
- **Data Protection**: Understand what personal information is collected
- **Informed Decisions**: Make privacy-conscious choices about online services

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Gemini API for enhanced AI analysis
export GEMINI_API_KEY="your_api_key_here"

# Optional: Custom model path for offline analysis
export MISTRAL_MODEL_PATH="mistralai/Mistral-7B-Instruct-v0.2"
```

### Backend Configuration
The backend automatically detects available AI models:
1. **Gemini Pro** (if API key provided)
2. **Mistral** (if model available)
3. **Rule-based** (fallback)

## 📊 Risk Scoring System

### Score Ranges
- **1-2**: Safe - Good privacy practices
- **3-4**: Moderate - Minor privacy concerns
- **5-6**: Caution - Some privacy concerns
- **7-8**: High Risk - Significant privacy concerns
- **9-10**: Dangerous - Critical privacy issues

### Scoring Factors
- **Website Type**: Social media, financial, educational
- **Legal Document Type**: Privacy policy, terms of service
- **Risk Indicators**: Privacy terms, legal clauses, data sharing
- **Form Analysis**: Sensitive field detection
- **Content Analysis**: Text length, suspicious patterns

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini Pro** for AI-powered analysis
- **BeautifulSoup** for web scraping
- **Selenium** for JavaScript-heavy sites
- **Flask** for the backend API

## 📞 Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](https://github.com/yourusername/shadowlens/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shadowlens/discussions)

---

**🔒 ShadowLens - Protecting Privacy in the Digital Age** #   S h a d o w L e n s  
 