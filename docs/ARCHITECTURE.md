# Architecture Documentation

## Overview

AI Sales Coaching System is an enterprise-level web application designed to analyze sales presentations using AI and speech processing technologies. The system provides a comprehensive analysis of sales effectiveness through multiple dimensions, helping sales teams improve their presentation skills.

## System Architecture

```
┌─────────────────────────┐
│  Frontend (Next.js)     │
│  React + Tailwind CSS   │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│   API Gateway (FastAPI) │
│  /api/v1/endpoints      │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│  Speech Processing      │
│  Whisper API / Local    │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│  AI Analysis            │
│  OpenAI / Claude /      │
│  DeepSeek APIs          │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│  Database (SQLite)      │
│  Recordings + Reports   │
└─────────────────────────┘
```

## Component Architecture

### Frontend Layer

**Framework**: Next.js 14 (App Router)
**Styling**: Tailwind CSS 3.x
**Language**: TypeScript

#### Pages

1. **Home Page** (`/`)
   - System introduction
   - Main upload area
   - Features showcase

2. **Upload Page** (`/upload`)
   - File upload interface
   - Drag and drop support
   - File validation

3. **Progress Page** (`/progress`)
   - Real-time processing status
   - Step-by-step visual feedback

4. **Report Page** (`/report`)
   - Radar chart visualization
   - Detailed analysis
   - Score breakdown

5. **History Page** (`/history`)
   - List of previous recordings
   - Quick report access

6. **Settings Page** (`/settings`)
   - API key management
   - Configuration options

### Backend Layer

**Framework**: FastAPI
**Language**: Python 3.11+

#### Main Components

1. **API Router** (`main.py`)
   - Handles HTTP requests
   - CORS configuration
   - Error handling

2. **Speech Analyzer** (`speech_analysis.py`)
   - Voice recognition
   - Speech rate analysis
   - Pause detection
   - Fluency scoring
   - Filler word detection

3. **AI Analyzer** (`ai_analyzer.py`)
   - Expression analysis
   - Content completeness check
   - Logic structure analysis
   - Customer understanding simulation
   - Persuasion analysis
   - Report generation

4. **Database** (`database.py`, `models.py`)
   - SQLite integration
   - ORM via SQLAlchemy
   - Recording and report storage

5. **Configuration** (`config.py`)
   - Environment variable management
   - API key configuration
   - System settings

### Speech Processing Pipeline

1. **Audio Upload**
   - File validation
   - Temporary storage

2. **Speech Recognition**
   - OpenAI Whisper API (primary)
   - Local Whisper model (fallback)

3. **Transcription**
   - Full text extraction
   - Segment analysis

4. **Speech Feature Extraction**
   - Speech rate calculation
   - Pause detection
   - Fluency scoring
   - Filler word identification

### AI Analysis Pipeline

1. **Input Preparation**
   - Transcript parsing
   - Feature extraction

2. **Expression Analysis**
   - Speech rate assessment
   - Pause analysis
   - Fluency scoring
   - Filler word detection

3. **Content Analysis**
   - Required point identification
   - Topic coverage
   - Information completeness

4. **Logic Analysis**
   - Structural evaluation
   - Flow assessment
   - Opening/closing effectiveness

5. **Customer Understanding**
   - Simulated customer response
   - Comprehension testing
   - Information clarity evaluation

6. **Persuasion Analysis**
   - Case study effectiveness
   - Value proposition assessment
   - Interest generation scoring

### Scoring System

```
Total Score = (0.2 × Expression) + (0.3 × Content) + (0.2 × Logic) + (0.2 × Customer) + (0.1 × Persuasion)
```

#### Weight Distribution
- **Expression**: 20%
- **Content**: 30%
- **Logic**: 20%
- **Customer Understanding**: 20%
- **Persuasion**: 10%

## Data Flow

### Recording Upload

```
User Upload
    ↓
File Validation
    ↓
Temporary Storage
    ↓
Speech Recognition
    ↓
Transcription
    ↓
Speech Analysis
    ↓
AI Analysis
    ↓
Report Generation
    ↓
Database Storage
    ↓
User Notification
```

### Analysis Process

```
Audio File
    ↓
Whisper API
    ↓
Transcript Text
    ↓
┌────────────────────┐
│ Speech Analysis    │
│ └─ Speed, Pauses,  │
│    Fluency, Fillers│
└────────────────────┘
    ↓
┌────────────────────┐
│ Content Analysis   │
│ └─ Coverage of     │
│    required points │
└────────────────────┘
    ↓
┌────────────────────┐
│ Logic Analysis     │
│ └─ Structure, Flow │
└────────────────────┘
    ↓
┌────────────────────┐
│ Customer Analysis  │
│ └─ Comprehension   │
└────────────────────┘
    ↓
┌────────────────────┐
│ Persuasion Analysis│
│ └─ Effectiveness   │
└────────────────────┘
    ↓
┌────────────────────┐
│ Report Generation  │
└────────────────────┘
    ↓
┌────────────────────┐
│ Score Calculation  │
└────────────────────┘
    ↓
Final Report
```

## Performance Considerations

### Speech Recognition
- Uses Whisper API for best accuracy
- Implements streaming for large files
- Fallback to local model for cost efficiency

### AI Analysis
- Optimizes API calls
- Implements caching for repeated requests
- Uses batch processing for efficiency

### Frontend Optimization
- Static site generation for landing page
- Dynamic imports for heavy components
- Image optimization
- Responsive design for all devices

## Security Features

1. **API Key Management**
   - Encrypted storage
   - Environment variable configuration
   - Regular rotation recommendations

2. **File Upload**
   - Strict validation
   - Virus checking
   - Limited file size

3. **Data Storage**
   - SQLite encryption options
   - Access control
   - Regular backups

4. **API Security**
   - CORS configuration
   - Rate limiting
   - Input validation

## Error Handling

1. **Speech Recognition**
   - Multiple retries
   - Fallback to local model
   - Error reporting

2. **API Calls**
   - Retry logic
   - Fallback mechanisms
   - User-friendly error messages

3. **Database**
   - Transaction management
   - Error recovery
   - Connection pooling

## Scalability

### Vertical Scaling
- Optimized speech recognition
- Database indexing
- Caching layers

### Horizontal Scaling
- Load balancing
- Distributed processing
- Cloud deployment options

### Infrastructure
- Docker containerization
- Kubernetes orchestration
- Cloud provider integration

## Monitoring and Analytics

1. **System Health**
   - API response time
   - Server metrics
   - Resource usage

2. **User Activity**
   - Upload frequency
   - Analysis duration
   - Report views

3. **Error Tracking**
   - Exception logging
   - Error patterns
   - Root cause analysis

## Future Enhancements

1. **Advanced Features**
   - Video analysis support
   - Multi-language support
   - Real-time coaching

2. **Performance Improvements**
   - GPU acceleration
   - Edge computing
   - Faster analysis

3. **Integration**
   - CRM integration
   - Learning management systems
   - Video conferencing tools

4. **Security**
   - Enhanced API security
   - Advanced encryption
   - Compliance certifications