# 🚀 ShadowLens Deployment Guide

## Quick Start

### 1. System Requirements
- Python 3.8+
- Node.js 16+
- Chrome browser
- 4GB RAM minimum
- 2GB disk space

### 2. Installation
```bash
# Clone and setup
git clone <repository>
cd shadowlens
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### 3. Configuration
Edit `.env` file:
```bash
# Optional: Add Gemini API key for cloud AI
GEMINI_API_KEY=your_api_key_here

# Backend settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Start Services
```bash
# Start backend
cd backend && python app.py

# Start dashboard (in new terminal)
cd dashboard && npm start

# Or use convenience script
./start_all.sh
```

### 5. Load Chrome Extension
1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select `chrome-extension/` folder

## 🧪 Testing

### Run Demo
```bash
python demo.py
```

### Test Backend
```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","forms":[],"text":"test","images":[]}'
```

### Test Dashboard
Visit: http://localhost:3000

## 🔧 Configuration Options

### Backend Configuration (`backend/config.py`)
- `USE_GEMINI`: Enable Google Gemini Pro API
- `USE_MISTRAL`: Enable local Mistral model
- `MAX_TEXT_LENGTH`: Maximum text to analyze
- `RISK_THRESHOLDS`: Risk score thresholds

### Chrome Extension Configuration
- `auto_scan`: Automatic scanning on EdTech sites
- `show_warnings`: Display privacy warnings
- `offline_mode`: Use local analysis only

## 📊 Monitoring

### Backend Health
- Endpoint: `GET /health`
- Status: 200 OK = Healthy
- Response includes AI model status

### Dashboard Metrics
- Total scans performed
- High-risk sites detected
- Average risk scores
- Recent activity log

## 🔒 Security Considerations

### Privacy
- No user data collected or stored
- All analysis performed anonymously
- Local storage only for scan history
- COPPA/FERPA/GDPR compliant

### Security
- HTTPS required for production
- Input validation on all endpoints
- Rate limiting enabled
- CORS configured for localhost

### API Keys
- Store in `.env` file (not in code)
- Use environment variables
- Rotate keys regularly
- Monitor usage

## 🚀 Production Deployment

### Backend (Flask)
```bash
# Using Gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t shadowlens-backend .
docker run -p 5000:5000 shadowlens-backend
```

### Dashboard (React)
```bash
# Build for production
cd dashboard
npm run build

# Serve with nginx
sudo apt install nginx
sudo cp build/* /var/www/html/
```

### Chrome Extension
1. Build extension: `cd chrome-extension && npm run build`
2. Package for Chrome Web Store
3. Submit for review

## 📈 Scaling

### Backend Scaling
- Use load balancer (nginx)
- Deploy multiple instances
- Use Redis for caching
- Monitor with Prometheus/Grafana

### Database (Optional)
- PostgreSQL for scan history
- MongoDB for analytics
- Redis for session storage

### AI Model Scaling
- Deploy Mistral on GPU servers
- Use cloud AI services (Gemini, OpenAI)
- Implement model caching
- Monitor API costs

## 🔍 Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check Python environment
source venv/bin/activate
python --version

# Check dependencies
pip list | grep flask

# Check logs
tail -f backend/logs/app.log
```

#### Chrome Extension Not Working
1. Check manifest.json syntax
2. Verify permissions in Chrome
3. Check console for errors
4. Reload extension

#### Dashboard Not Loading
```bash
# Check Node.js
node --version
npm --version

# Reinstall dependencies
cd dashboard
rm -rf node_modules
npm install

# Check for port conflicts
lsof -i :3000
```

### Logs
- Backend: `backend/logs/`
- Dashboard: Browser console
- Extension: Chrome DevTools

## 📚 API Documentation

### Endpoints

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "ai_model": "rule-based",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### `POST /analyze`
Privacy analysis endpoint
```json
{
  "url": "https://example.com",
  "forms": [{"fields": []}],
  "text": "page content",
  "images": [],
  "riskIndicators": []
}
```

Response:
```json
{
  "summary": "Analysis summary",
  "risk_score": 5,
  "recommendation": "Caution",
  "red_flags": ["flag1", "flag2"],
  "privacy_threats": ["threat1"],
  "brand_impersonation": ["impersonation1"],
  "data_collection_analysis": "analysis text",
  "student_safety_concerns": ["concern1"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎯 Performance Optimization

### Backend
- Enable response caching
- Use async processing
- Optimize AI model loading
- Implement connection pooling

### Frontend
- Enable code splitting
- Use lazy loading
- Optimize bundle size
- Implement service workers

### Extension
- Minimize DOM queries
- Use efficient selectors
- Implement debouncing
- Cache analysis results

## 📞 Support

### Documentation
- README.md: Main documentation
- SECURITY.md: Security details
- docs/business-case.md: Business case

### Contact
- Issues: GitHub issues
- Security: security@shadowlens.com
- Business: business@shadowlens.com

### Community
- Discord: ShadowLens Community
- Twitter: @ShadowLensAI
- LinkedIn: ShadowLens

---

**🔒 ShadowLens: Protecting Student Privacy, One Scan at a Time** 