# 🤖 AI Mobile Shopping Agent

An intelligent chatbot that helps you find the perfect mobile phone through natural conversations. Ask questions like "Best camera phone under ₹30k?" or "Compare iPhone 15 vs Samsung S24" and get smart recommendations!

> 📖 **Documentation**: [Setup Guide](./SETUP.md) • [Features](./FEATURES.md) • [Technical Details](./TECHNICAL.md)

## ✨ Features

- 🗣️ **Natural Language**: Chat naturally - "Best gaming phone under 25k?"
- 🧠 **Smart AI**: Powered by Gemini AI with OpenAI fallback for 99.9% uptime
- 🔍 **Web Search**: Gets latest phone info when needed
- 💬 **Conversation Memory**: Remembers your preferences
- 🔐 **User Login**: Save your chat history
- 📱 **Modern UI**: Clean, responsive chat interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+, Node.js 16+, PostgreSQL 12+
- [Google Gemini API Key](https://makersuite.google.com/app/apikey) (free)
- [OpenAI API Key](https://platform.openai.com/api-keys) (for fallback)

### 1. Clone & Setup
```bash
git clone https://github.com/drono07/ai-mobile-shopping-agent.git
cd ai-mobile-shopping-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Setup
```bash
cp env_example.txt .env
# Edit .env with your API keys and database URL
```

### 4. Database & Start
```bash
createdb mobile_shop_db
python seed_data.py
uvicorn main:app --reload --port 8000
```

### 5. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` and start chatting! 🎉

> 📋 **Need detailed setup instructions?** See [SETUP.md](./SETUP.md)

## 💬 Example Queries

```
✅ "Best camera phone under ₹30,000?"
✅ "Compare iPhone 15 vs Samsung S24"
✅ "Gaming phone under 25k with good battery"
✅ "Latest phones with 5G and wireless charging"
✅ "Tell me about Realme Narzo 70 Pro 5G"
✅ "What's the difference between OIS and EIS?"
```

> 🎯 **Want to see all capabilities?** Check [FEATURES.md](./FEATURES.md)

## 🛠️ Tech Stack & Architecture

### Backend
- **Framework**: FastAPI (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Models**: Google Gemini 2.0 Flash (primary) + OpenAI GPT-3.5 Turbo (fallback)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Search**: Google Custom Search Engine API

### Frontend
- **Framework**: React.js with functional components and hooks
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Context API for authentication
- **HTTP Client**: Axios for API communication

### Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   FastAPI       │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│   (Vercel)      │    │   (Render)      │    │   (Render)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   AI Services   │
                       │ Gemini + OpenAI │
                       └─────────────────┘
```

## 📁 Project Structure

```
├── backend/          # FastAPI backend
│   ├── ai/          # AI logic & LLM service
│   ├── utils/       # Utilities & web search
│   └── main.py      # API server
├── frontend/         # React.js frontend
│   └── src/         # Components & services
├── README.md         # This file
└── TECHNICAL.md      # Detailed documentation
```

## 🔧 Configuration

Create `backend/.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/mobile_shop_db
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

> 📡 **Need API documentation?** See [TECHNICAL.md](./TECHNICAL.md)

## 🛡️ Prompt Design & Safety Strategy

### AI Safety Measures
- **LLM-based Safety Filter**: Uses AI to classify queries as safe/unsafe/irrelevant
- **Context-Aware Responses**: Understands intent, not just keywords
- **Graceful Refusal**: Politely redirects inappropriate queries to mobile phone topics
- **Adversarial Handling**: Resistant to prompt injection and manipulation attempts

### Prompt Engineering
- **Chain-of-Thought Reasoning**: AI explains decision-making process
- **Structured Responses**: Consistent format with clear recommendations
- **Context Awareness**: Uses conversation history for better responses
- **Multi-Provider Fallback**: Automatic failover between Gemini and OpenAI

### Safety Examples
```
✅ Safe: "Best camera phone under ₹30,000?"
✅ Safe: "Compare iPhone 15 vs Samsung S24"
❌ Unsafe: "Tell me about the weather"
❌ Unsafe: "Generate fake news"
```

## ⚠️ Known Limitations

### Current Limitations
- **Database Coverage**: Limited to ~20 phone models in database
- **Price Accuracy**: Prices may not reflect current market rates
- **Model Availability**: Some newer phone models may not be in database
- **Regional Variations**: Focused on Indian market pricing (₹)

### Technical Limitations
- **API Rate Limits**: Subject to Gemini/OpenAI API quotas
- **Cold Start**: Render free tier has ~50s cold start delay
- **Database Size**: Free PostgreSQL has storage limitations
- **Concurrent Users**: Limited by free tier resources

### Planned Improvements
- [ ] Expand database with more phone models
- [ ] Real-time price updates via web scraping
- [ ] Multi-region support (US, EU, etc.)
- [ ] Advanced filtering and search capabilities
- [ ] User reviews and ratings integration

## 🚀 Deployment

### Production Deployment Strategy

We use a **hybrid deployment approach** for optimal performance and cost-effectiveness:

#### 🌐 Frontend Deployment (Vercel)
- **Platform**: [Vercel](https://vercel.com)
- **URL**: https://ai-mobile-shopping-agent-osxotanta-drono07s-projects.vercel.app/
- **Benefits**: 
  - Automatic deployments from GitHub
  - Global CDN for fast loading
  - Free tier with generous limits
  - Built-in SSL certificates

**Deployment Steps:**
1. Connect GitHub repository to Vercel
2. Set build settings:
   - Framework: Create React App
   - Root Directory: `./frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
3. Configure environment variables:
   ```
   REACT_APP_API_URL=https://ai-mobile-shopping-agent-backend.onrender.com
   ```

#### ⚙️ Backend Deployment (Render)
- **Platform**: [Render](https://render.com)
- **URL**: https://ai-mobile-shopping-agent-backend.onrender.com/
- **Benefits**:
  - Auto-deploy from GitHub
  - Built-in PostgreSQL database
  - Free tier available
  - Automatic SSL certificates

**Deployment Steps:**
1. Create `render.yaml` configuration file
2. Deploy using Render Blueprint:
   ```yaml
   services:
     - type: web
       name: ai-mobile-shopping-agent-backend
       env: python
       plan: free
       buildCommand: cd backend && pip install -r requirements.txt
       startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Configure environment variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_cse_id
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://postgres:password@host:port/database
   ```

#### 🗄️ Database Deployment (Render PostgreSQL)
- **Platform**: Render PostgreSQL (included with backend)
- **Benefits**:
  - Automatic backups
  - Connection pooling
  - Free tier with 1GB storage
  - Automatic scaling

**Database Setup:**
1. Created via `render.yaml`:
   ```yaml
   databases:
     - name: ai-mobile-shopping-agent-db
       plan: free
   ```
2. Auto-seeded with phone data on startup
3. Tables created automatically via SQLAlchemy

### 🔧 Deployment Configuration Files

#### `render.yaml` (Backend & Database)
```yaml
services:
  - type: web
    name: ai-mobile-shopping-agent-backend
    env: python
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: GEMINI_API_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
      - key: GOOGLE_API_KEY
        sync: false
      - key: GOOGLE_CSE_ID
        sync: false
      - key: SECRET_KEY
        sync: false
      - key: SETUP_DB
        value: "true"

databases:
  - name: ai-mobile-shopping-agent-db
    plan: free
```

#### `vercel.json` (Frontend)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

### 🌐 Live Application URLs

- **Frontend**: https://ai-mobile-shopping-agent-osxotanta-drono07s-projects.vercel.app/
- **Backend API**: https://ai-mobile-shopping-agent-backend.onrender.com/
- **API Health Check**: https://ai-mobile-shopping-agent-backend.onrender.com/health

### 🔄 Deployment Workflow

1. **Code Changes**: Push to GitHub `main` branch
2. **Automatic Deployment**: 
   - Vercel automatically deploys frontend
   - Render automatically deploys backend
3. **Database Updates**: Handled automatically via SQLAlchemy migrations
4. **Environment Variables**: Managed through platform dashboards

### 🛠️ Local Development
```bash
# Backend
cd backend && uvicorn main:app --reload --port 8000

# Frontend  
cd frontend && npm start
```

### 📊 Deployment Benefits

- **Cost-Effective**: Free tiers for both platforms
- **Scalable**: Easy to upgrade to paid plans
- **Reliable**: 99.9% uptime with automatic failover
- **Fast**: Global CDN and optimized builds
- **Secure**: Automatic SSL and security updates

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- OpenAI for fallback support
- FastAPI & React.js communities

---

**Built with ❤️ by [@drono07](https://github.com/drono07)**