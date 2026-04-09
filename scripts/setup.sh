#!/bin/bash
# Self-Hosted AI API - Linux/Mac Setup Script
# Run this script to set up the development environment

set -e

echo "🚀 Self-Hosted AI API - Setup Script"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama not found. Installing...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✅ Ollama installed${NC}"
else
    echo -e "${GREEN}✅ Ollama found: $(ollama --version)${NC}"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Copy environment file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created. Please edit with your values.${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Pull default model
echo -e "${YELLOW}📥 Checking for default model...${NC}"
if ! ollama list | grep -q "qwen:1.8b"; then
    echo "Pulling qwen:1.8b model (this may take a few minutes)..."
    ollama pull qwen:1.8b
    echo -e "${GREEN}✅ Model pulled${NC}"
else
    echo -e "${GREEN}✅ Default model already exists${NC}"
fi

echo ""
echo "===================================="
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start Ollama: ollama serve"
echo "3. Run the API: python src/app.py"
echo "4. Test: curl http://localhost:8000/health"
echo ""
