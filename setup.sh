#!/bin/bash

# ShadowLens Setup Script
# Installs and configures all components

set -e

echo "🔒 ShadowLens Setup Script"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python 3.8+ found: $(python3 --version)"
        else
            print_error "Python 3.8+ required, found: $(python3 --version)"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js not found. Please install Node.js 16+"
        exit 1
    fi
}

# Setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    print_success "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r backend/requirements.txt
    print_success "Python dependencies installed"
}

# Setup Node.js dependencies
setup_node_env() {
    print_status "Setting up Node.js environment..."
    
    cd dashboard
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "Node.js dependencies installed"
    else
        print_status "Node.js dependencies already installed"
    fi
    cd ..
}

# Create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# ShadowLens Environment Configuration

# Flask Backend
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
SECRET_KEY=shadowlens-secret-key-change-in-production

# AI Models
GEMINI_API_KEY=your-gemini-api-key-here
MISTRAL_MODEL_PATH=mistralai/Mistral-7B-Instruct-v0.2

# Analysis Settings
MAX_TEXT_LENGTH=3000
MAX_FORMS_PER_SITE=10
MAX_IMAGES_PER_SITE=50

# Risk Thresholds
RISK_SAFE_THRESHOLD=3
RISK_CAUTION_THRESHOLD=6
RISK_DANGEROUS_THRESHOLD=7

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=shadowlens.log

# CORS Settings
CORS_ORIGINS=http://localhost:3000,chrome-extension://*
EOF
        print_success "Environment file created: .env"
        print_warning "Please edit .env and add your Gemini API key if using cloud AI"
    else
        print_status "Environment file already exists"
    fi
}

# Create Chrome extension icons
create_extension_icons() {
    print_status "Creating Chrome extension icons..."
    
    # Create icons directory
    mkdir -p chrome-extension/icons
    
    # Create placeholder icons (you should replace these with actual icons)
    for size in 16 32 48 128; do
        if [ ! -f "chrome-extension/icons/icon${size}.png" ]; then
            # Create a simple placeholder icon using ImageMagick if available
            if command -v convert &> /dev/null; then
                convert -size ${size}x${size} xc:transparent \
                    -fill '#667eea' -draw "circle $(($size/2)),$(($size/2)) $(($size/2)),$(($size/4))" \
                    -fill white -pointsize $(($size/3)) -gravity center -annotate 0 "🔒" \
                    chrome-extension/icons/icon${size}.png
            else
                # Create empty files as placeholders
                touch chrome-extension/icons/icon${size}.png
                print_warning "Created placeholder icon. Please replace with actual icon."
            fi
        fi
    done
    
    print_success "Chrome extension icons created"
}

# Create startup scripts
create_startup_scripts() {
    print_status "Creating startup scripts..."
    
    # Backend startup script
    cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source ../venv/bin/activate
python app.py
EOF
    chmod +x start_backend.sh
    
    # Dashboard startup script
    cat > start_dashboard.sh << 'EOF'
#!/bin/bash
cd dashboard
npm start
EOF
    chmod +x start_dashboard.sh
    
    # Combined startup script
    cat > start_all.sh << 'EOF'
#!/bin/bash
echo "Starting ShadowLens..."

# Start backend in background
echo "Starting backend..."
./start_backend.sh &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start dashboard
echo "Starting dashboard..."
./start_dashboard.sh &
DASHBOARD_PID=$!

echo "ShadowLens started!"
echo "Backend: http://localhost:5000"
echo "Dashboard: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $DASHBOARD_PID; exit" INT
wait
EOF
    chmod +x start_all.sh
    
    print_success "Startup scripts created"
}

# Create test script
create_test_script() {
    print_status "Creating test script..."
    
    cat > test_system.py << 'EOF'
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
EOF
    
    print_success "Test script created"
}

# Main setup function
main() {
    echo ""
    print_status "Starting ShadowLens setup..."
    
    # Check prerequisites
    check_python
    check_node
    
    # Setup environments
    setup_python_env
    setup_node_env
    
    # Create configuration files
    create_env_file
    create_extension_icons
    create_startup_scripts
    create_test_script
    
    echo ""
    print_success "ShadowLens setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file and add your Gemini API key (optional)"
    echo "2. Load the Chrome extension from chrome-extension/ folder"
    echo "3. Run './start_all.sh' to start all services"
    echo "4. Run 'python test_system.py' to test the system"
    echo ""
    echo "Documentation: README.md"
    echo "Support: Check the logs for any issues"
}

# Run main function
main 