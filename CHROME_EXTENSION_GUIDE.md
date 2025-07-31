# 🔒 ShadowLens Chrome Extension Guide

## Overview
ShadowLens Chrome Extension automatically detects and analyzes privacy policies, terms of service, and other legal documents on any website. It provides real-time privacy risk assessment without any manual input.

## 🚀 Installation

### Step 1: Start the Backend Server
```bash
cd /Users/lingesh/astrixxx/hackathon
source venv/bin/activate
export GEMINI_API_KEY="AIzaSyCpxYzcgkVPk1X8QiC05Rc6-KNd-np81i8"
python3 backend/app.py
```

### Step 2: Load the Extension in Chrome
1. **Open Chrome** and go to `chrome://extensions/`
2. **Enable "Developer mode"** (toggle in top right)
3. **Click "Load unpacked"**
4. **Select the `chrome-extension` folder:**
   ```
   /Users/lingesh/astrixxx/hackathon/chrome-extension
   ```

## 🎯 How It Works

### Automatic Detection
- **Legal Documents**: Automatically detects privacy policies, terms of service, cookie policies
- **Any Website**: Works on any website, not just educational ones
- **Real-time Analysis**: Analyzes content as soon as you visit a page

### What It Analyzes
1. **Privacy Policies**: Detects data collection practices
2. **Terms of Service**: Identifies concerning legal clauses
3. **Form Fields**: Analyzes sensitive data collection
4. **Risk Indicators**: Flags privacy threats and legal concerns

## 📊 Understanding the Results

### Risk Score (0-10)
- **🟢 0-3**: Safe - Good privacy practices
- **🟡 4-5**: Moderate - Some privacy concerns
- **🟠 6-7**: Caution - Significant privacy concerns
- **🔴 8-10**: Dangerous - Critical privacy issues

### Analysis Categories
- **🔒 Privacy Threats**: Data collection, tracking, marketing
- **⚖️ Legal Concerns**: Concerning legal terms and clauses
- **📝 Form Analysis**: Sensitive field detection
- **🔍 Privacy Links**: Found privacy policy links

## 🧪 Testing the Extension

### Test URLs
1. **Facebook Privacy Policy**: `https://www.facebook.com/privacy/policy/`
2. **Google Terms**: `https://policies.google.com/terms`
3. **Any Educational Site**: `https://coursera.org`
4. **Any Website**: Just visit any site and check for privacy links

### Expected Results
- **Facebook**: High risk (8-10) - Extensive data collection
- **Google**: Moderate risk (4-6) - Standard tech company practices
- **Educational Sites**: Variable risk based on data collection

## 🔧 Features

### Automatic Analysis
- ✅ Detects legal documents automatically
- ✅ Analyzes privacy policies and terms
- ✅ Identifies sensitive form fields
- ✅ Flags concerning legal clauses
- ✅ Provides risk scoring

### Visual Indicators
- **Badge Colors**: Extension icon changes color based on risk
- **Risk Score**: Large number display in popup
- **Threat Lists**: Detailed breakdown of privacy concerns
- **Form Analysis**: Count of sensitive fields

### Privacy Links Detection
- Automatically finds privacy policy links on any page
- Shows clickable links in the popup
- Helps users navigate to legal documents

## 🛠️ Troubleshooting

### Extension Not Working
1. **Check Backend**: Ensure `python3 backend/app.py` is running
2. **Check Console**: Open Chrome DevTools to see error messages
3. **Reload Extension**: Go to `chrome://extensions/` and click reload
4. **Check Permissions**: Ensure extension has access to the website

### No Analysis Results
1. **Wait for Loading**: Analysis takes 5-10 seconds
2. **Check Network**: Ensure backend is accessible
3. **Refresh Page**: Try refreshing the webpage
4. **Manual Trigger**: Click the extension icon to trigger analysis

### Backend Connection Issues
1. **Check Port**: Ensure nothing else is using port 5000
2. **Check API Key**: Verify GEMINI_API_KEY is set
3. **Check Firewall**: Ensure localhost:5000 is accessible
4. **Restart Backend**: Stop and restart the Python server

## 📈 Advanced Usage

### Custom Analysis
- Visit any website with privacy policies
- Click the ShadowLens icon
- Review the detailed analysis
- Check for privacy policy links

### Privacy Policy Discovery
- The extension automatically finds privacy policy links
- Click on links in the popup to read policies
- Get instant analysis of legal documents

### Risk Assessment
- Understand what data websites collect
- Identify concerning legal terms
- Make informed decisions about data sharing

## 🔒 Privacy & Security

### What ShadowLens Does
- ✅ Analyzes website content for privacy risks
- ✅ Identifies data collection practices
- ✅ Flags concerning legal terms
- ✅ Provides risk scoring

### What ShadowLens Does NOT Do
- ❌ Collect personal data
- ❌ Store browsing history
- ❌ Share data with third parties
- ❌ Track user behavior

### Data Processing
- All analysis happens locally or on your backend
- No data is sent to external services (except Gemini API for analysis)
- Extension only reads publicly available website content

## 🎯 Use Cases

### For Students
- Check educational platform privacy policies
- Understand data collection by learning tools
- Make informed decisions about online learning

### For Educators
- Assess privacy practices of educational tools
- Ensure student data protection
- Choose privacy-respecting platforms

### For Everyone
- Understand website privacy practices
- Identify concerning legal terms
- Make informed decisions about data sharing

## 📞 Support

If you encounter issues:
1. Check the Chrome DevTools console for errors
2. Verify the backend server is running
3. Test with the provided test URLs
4. Check the extension permissions

---

**🔒 ShadowLens: Your Privacy Guardian for the Web** 