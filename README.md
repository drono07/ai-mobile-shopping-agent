# 🤖 AI Mobile Shopping Agent

An intelligent chatbot that helps you find the perfect mobile phone through natural conversations. Ask questions like "Best camera phone under ₹30k?" or "Compare iPhone 15 vs Samsung S24" and get smart recommendations!

> 📖 **Documentation**: [Setup Guide](./SETUP.md) • [API Reference](./API.md) • [Features](./FEATURES.md) • [Technical Details](./TECHNICAL.md)

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

## 🛠️ Tech Stack

- **Backend**: FastAPI + PostgreSQL + SQLAlchemy
- **Frontend**: React.js + Tailwind CSS
- **AI**: Google Gemini 2.0 Flash + OpenAI GPT-3.5 Turbo (fallback)
- **Search**: Google Custom Search Engine

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

> 📡 **Need API documentation?** See [API.md](./API.md)

## 🚀 Deployment

### Quick Deploy with Docker
```bash
docker-compose up -d
```

### Manual Deploy
- **Backend**: Deploy to Vercel, Railway, or Heroku
- **Frontend**: Deploy to Vercel, Netlify, or GitHub Pages
- **Database**: Use Supabase, Railway, or AWS RDS

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