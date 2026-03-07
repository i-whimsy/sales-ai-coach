# AI Sales Coaching System - Architecture Documentation

## 1. System Overview
AI Sales Coaching System is a web application that analyzes sales recordings to provide coaching feedback using AI. The system consists of a mock backend server and a Vue 3 frontend, designed to help sales professionals improve their communication skills through AI-driven analysis.

## 2. System Architecture
The system follows a typical client-server architecture:
- **Frontend**: Vue 3 application with Vite build tool, using Tailwind CSS for styling and Vue Router for navigation
- **Backend**: Node.js/Express mock server providing REST API endpoints
- **Data Storage**: In-memory mock data (in production, this would be a persistent database like PostgreSQL or MongoDB)
- **AI Integration**: Currently using mock data, designed to integrate with Whisper for transcription and OpenAI/Claude/DeepSeek for analysis

## 3. Main Modules & Responsibilities

### 3.1 Backend Modules (mock-server.js)
- **Server Setup**: Express server with CORS enabled and JSON parsing configured
- **Mock Data Management**: In-memory storage for recordings and analysis reports
- **API Endpoints**: 
  - `/health` - Health check endpoint
  - `/api/v1/recordings` - CRUD operations for recording management
  - `/api/v1/recordings/:id/analyze` - Trigger AI analysis of recordings
  - `/api/v1/api-config` - Manage API keys for AI services
  - `/api/v1/scoring-config` - Configure scoring weights for different evaluation criteria

### 3.2 Frontend Modules
- **App Layout**: Main application structure with header, navigation menu, and footer
- **Views**:
  - `Home.vue` - Landing page with system introduction
  - `Upload.vue` - File upload functionality with validation
  - `History.vue` - List of previously uploaded recordings
  - `Analyze.vue` - Analysis progress interface
  - `Report.vue` - Detailed analysis report with scores and feedback
  - `Settings.vue` - System configuration for API keys and scoring weights
- **UI Components**: Reusable UI components (tabs, buttons, etc.)

## 4. Key Data Flow

### 4.1 Recording Upload Flow
1. User selects or drags a recording file in the frontend
2. Frontend validates file format and size (supports MP3, WAV, M4A; max 200MB)
3. Frontend sends POST request to `/api/v1/recordings` with file data
4. Backend creates recording entry and returns ID
5. Frontend displays success message with options to view history or start analysis

### 4.2 Recording Analysis Flow
1. User clicks "Analyze" on a recording in history
2. Frontend sends POST request to `/api/v1/recordings/:id/analyze`
3. Backend simulates AI analysis delay
4. Backend returns mock analysis report with scores and feedback
5. Frontend navigates to report page to display detailed results

## 5. Model Configuration & Call Logic

### 5.1 Current Implementation (Mock)
- The system uses static mock data for analysis results
- No actual AI model calls are made in the current configuration
- All analysis endpoints return pre-defined response data

### 5.2 Production Implementation
In a production environment, the system would:
1. Use Whisper API to transcribe audio recordings to text
2. Send transcript to LLM API (OpenAI/Claude/DeepSeek) for analysis
3. Calculate total score based on configured weights (expression: 20%, content: 30%, logic: 20%, customer: 20%, persuasion: 10%)
4. Return structured report with strengths, weaknesses, and suggestions

## 6. Frontend-Backend Relationship
- **Communication**: Frontend uses Axios to make HTTP requests to backend REST API
- **CORS**: Backend is configured with CORS to allow cross-origin requests from frontend
- **Deployment**: Frontend can be deployed separately or served by the backend Express server
- **Responsiveness**: Frontend is built with responsive design principles to work on desktop and mobile devices

## 7. Important Design Decisions

### 7.1 Mock-First Development
- The system provides a complete mock backend to enable frontend development without requiring AI API keys or paid services
- Mock data closely mimics expected production responses

### 7.2 Modular Architecture
- Frontend components are organized by feature for maintainability
- Backend endpoints are grouped by resource type (RESTful design)

### 7.3 User Experience Focus
- File upload with drag-and-drop support and real-time validation
- Progress indicators for upload and analysis processes
- Clear visual hierarchy and responsive design with Tailwind CSS
- Intuitive navigation with clear call-to-action buttons

### 7.4 Configurable System
- API key management for different AI service providers
- Customizable scoring weights to adapt to different business needs
- Extensible design to support additional AI models in the future

## 8. Technology Stack

### 8.1 Backend
- **Node.js**: Runtime environment
- **Express**: Web application framework
- **CORS**: Cross-origin resource sharing middleware
- **Nodemon**: Development server with auto-reload

### 8.2 Frontend
- **Vue 3**: Progressive JavaScript framework with Composition API
- **Vue Router**: Client-side routing
- **Vite**: Build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **Lucide Vue Next**: Icon library

## 9. Future Enhancements
- Integration with real AI transcription and analysis services
- Persistent database storage for recordings and reports
- User authentication and authorization
- Team collaboration features
- Advanced analytics and reporting
- Integration with CRM systems
- Mobile application support
