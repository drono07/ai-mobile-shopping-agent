# 🚀 Setup Guide

Detailed setup instructions for the AI Mobile Shopping Agent.

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 16+** and npm installed  
3. **PostgreSQL 12+** installed and running
4. **Google Gemini API Key** (free tier available)
5. **OpenAI API Key** (for fallback support)

## 🔧 Detailed Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/drono07/ai-mobile-shopping-agent.git
cd ai-mobile-shopping-agent
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env file with your credentials
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/mobile_shop_db
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_cse_id_here
SECRET_KEY=your_secret_key_here
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb mobile_shop_db

# Alternative: Using psql
psql -U postgres
CREATE DATABASE mobile_shop_db;
\q
```

### 5. Seed Database

```bash
# Run the seed script to populate with sample phone data
python seed_data.py

# Create authentication tables
python create_auth_tables.py
```

### 6. Start Backend Server

```bash
# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Alternative: Using Python directly
python main.py
```

The backend will be available at `http://localhost:8000`

### 7. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🔑 Getting API Keys

### Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your OpenAI account
3. Create a new API key
4. Copy the key and add it to your `.env` file

### Google Custom Search Engine

1. Visit [Google Custom Search Engine](https://cse.google.com/cse/)
2. Create a new search engine
3. Get your API key from [Google Cloud Console](https://console.cloud.google.com/)
4. Get your CSE ID from the search engine settings

## 🐳 Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🧪 Testing the Setup

### Backend API Testing

```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Get all phones
curl -X GET "http://localhost:8000/phones"

# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Best camera phone under 30000?"}'
```

### Frontend Testing

1. Open your browser and navigate to `http://localhost:3000`
2. Try the sample queries in the chat interface
3. Test phone comparison functionality
4. Verify user registration and login

## 🔧 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if PostgreSQL is running
- Verify database credentials in `.env`
- Ensure all Python dependencies are installed
- Check if port 8000 is available

**Frontend won't connect:**
- Verify backend is running on port 8000
- Check CORS settings in backend
- Ensure API URL is correct in frontend
- Check if port 3000 is available

**Database connection errors:**
- Verify PostgreSQL is running
- Check database credentials
- Ensure database exists
- Check if user has proper permissions

**AI responses are slow:**
- Check Gemini API key is valid
- Verify internet connection
- Consider API rate limits
- Check OpenAI API key for fallback

**Authentication issues:**
- Verify SECRET_KEY is set in `.env`
- Check JWT token configuration
- Ensure user tables are created

### Logs and Debugging

**Backend logs:**
```bash
# View FastAPI logs
uvicorn main:app --reload --log-level debug

# Check database logs
tail -f /var/log/postgresql/postgresql-*.log
```

**Frontend logs:**
```bash
# View React logs in browser console
# Check Network tab for API calls
```

## 📊 Performance Optimization

### Backend Optimization
- Use connection pooling for database
- Enable Redis caching (optional)
- Optimize database queries
- Use async/await properly

### Frontend Optimization
- Enable code splitting
- Use React.memo for components
- Optimize bundle size
- Enable service worker (optional)

## 🔒 Security Considerations

- Never commit `.env` files
- Use strong SECRET_KEY
- Enable HTTPS in production
- Validate all user inputs
- Use rate limiting
- Keep dependencies updated

## 🚀 Production Deployment

### Environment Variables for Production
```env
DATABASE_URL=postgresql://user:pass@prod-db:5432/mobile_shop_db
GEMINI_API_KEY=your_prod_gemini_key
OPENAI_API_KEY=your_prod_openai_key
SECRET_KEY=your_strong_secret_key
ENVIRONMENT=production
```

### Database Migration
```bash
# Run migrations (if using Alembic)
alembic upgrade head
```

### Static Files
```bash
# Build frontend for production
cd frontend
npm run build
```

---

For more detailed technical information, see [TECHNICAL.md](./TECHNICAL.md)
