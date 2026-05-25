#!/bin/bash
# Quick Start Script for Greatest Game Agent
# Run this from the project-files directory

echo "🎮 Greatest Game Agent - Quick Setup"
echo "======================================"
echo ""

# Check Python
echo "✓ Checking Python..."
python --version

# Check Node
echo "✓ Checking Node.js..."
node --version

echo ""
echo "📦 Installing Backend Dependencies..."
cd backend
if [ ! -d "venv" ]; then
  python -m venv venv
fi
source venv/Scripts/activate
pip install -r requirements.txt

echo ""
echo "📦 Installing Frontend Dependencies..."
cd ../frontend
npm install

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Create .env file in backend/ with your API keys"
echo "2. Run migrations: cd backend && python manage.py migrate"
echo "3. Create superuser: python manage.py createsuperuser"
echo "4. Start backend: python manage.py runserver"
echo "5. In new terminal, start frontend: cd frontend && npm start"
echo ""
echo "Application will be at http://localhost:3000"
