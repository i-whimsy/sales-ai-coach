# Sales AI Coach

🎙️ **AI-driven sales presentation analysis and coaching system**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start

### One-Click Start (Windows)

```bash
# Double-click to start
start-all.bat
```

### Manual Start

```bash
# Terminal 1: Start backend
cd backend
python main.py

# Terminal 2: Start frontend
cd frontend-vue
npm run dev

# Open browser
http://localhost:3002
```

---

## 📦 Features

### Core Capabilities

- **🎵 Audio Upload**: Support WAV, MP3, M4A formats
- **📝 Speech-to-Text**: Whisper-powered transcription
- **📊 Content Analysis**: AI-powered content evaluation
- **🎯 Scoring**: Multi-dimensional scoring system
- **📈 Reports**: Detailed analysis reports
- **⚙️ Configurable**: Customizable prompts and weights

### Analysis Dimensions

- **Expression Quality**: Speech rate, pauses, fluency
- **Content Completeness**: Key sections coverage
- **Logical Structure**: Presentation flow
- **Customer Understanding**: Clarity assessment
- **Persuasion**: Effectiveness evaluation

---

## 🏗️ Architecture

```
sales-ai-coach/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── models.py        # Database models
│   ├── speech_analysis.py
│   ├── ai_analyzer.py
│   └── content_analyzer.py
├── frontend-vue/         # Vue 3 frontend
│   ├── src/
│   │   ├── views/
│   │   └── components/
│   └── package.json
└── sales_coach.db        # SQLite database
```

---

## 💻 Usage

### 1. Upload Recording

1. Go to "Upload Recording" page
2. Select audio file (WAV/MP3/M4A)
3. Choose analysis model (optional)
4. Click "Upload"

### 2. View Analysis

1. Go to "History" page
2. Click on a recording
3. View detailed report

### 3. Configure Analysis

1. Go to "Settings" page
2. Adjust scoring weights
3. Configure prompt templates

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/config.py`:

```python
# API Keys
OPENAI_API_KEY = "your-key"
DEEPSEEK_API_KEY = "your-key"

# Database
DATABASE_URL = "sqlite:///./sales_coach.db"
```

### Frontend Configuration

Edit `frontend-vue/.env`:

```env
VITE_API_BASE_URL=http://localhost:8001/api/v1
```

---

## 🛠️ Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

### Frontend Setup

```bash
cd frontend-vue

# Install dependencies
npm install

# Run dev server
npm run dev
```

---

## 📊 API Endpoints

### Recordings

- `POST /api/v1/recordings` - Upload recording
- `GET /api/v1/recordings` - List all recordings
- `GET /api/v1/recordings/{id}` - Get recording details
- `POST /api/v1/recordings/{id}/analyze` - Analyze recording
- `GET /api/v1/recordings/{id}/logs` - Get analysis logs

### Models

- `GET /api/v1/models` - List all models
- `POST /api/v1/models` - Create model
- `PUT /api/v1/models/{id}` - Update model
- `POST /api/v1/models/{id}/test` - Test model

### Settings

- `GET /api/v1/scoring-config` - Get scoring config
- `PUT /api/v1/scoring-config` - Update scoring config
- `GET /api/v1/tasks` - List task configs
- `PUT /api/v1/tasks/{name}` - Update task config

---

## 🤝 Related Projects

### Audio Metrics CLI

For command-line audio analysis, check out:

- **Project**: [audio-metrics-cli](https://github.com/i-whimsy/audio-metrics-cli)
- **Description**: Cross-platform CLI tool for speech metrics extraction
- **Installation**: `pip install audio-metrics-cli` (after PyPI release)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech-to-text
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Vue 3](https://vuejs.org/) - Frontend framework

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/i-whimsy/sales-ai-coach/issues)
- **Discussions**: [GitHub Discussions](https://github.com/i-whimsy/sales-ai-coach/discussions)

---

**Built with ❤️ by OpenClaw Team**
