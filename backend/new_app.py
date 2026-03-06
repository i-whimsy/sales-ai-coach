"""AI Sales Coaching System - New Backend API
A simplified and improved version of the backend service
"""

import os
import json
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np

# Create FastAPI app
app = FastAPI(
    title="AI Sales Coaching System",
    version="2.0.0",
    description="A simplified and improved AI sales coaching backend service"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploads"
REPORTS_DIR = "reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# In-memory database
recordings_db = {}
config_db = {
    "api_keys": {},
    "scoring_weights": {
        "expression": 0.20,
        "content": 0.30,
        "logic": 0.20,
        "customer": 0.20,
        "persuasion": 0.10
    }
}

# Mock data
def generate_mock_report(transcript: str = "") -> Dict[str, Any]:
    """Generate a mock analysis report"""
    
    # Random scores within realistic ranges
    scores = {
        "expression": np.random.uniform(75, 95),
        "content": np.random.uniform(70, 90),
        "logic": np.random.uniform(75, 95),
        "customer": np.random.uniform(70, 85),
        "persuasion": np.random.uniform(80, 95)
    }
    
    # Calculate total score using weights
    total_score = sum(
        scores[key] * config_db["scoring_weights"][key]
        for key in scores
    )
    
    # Generate sample strengths
    strengths = [
        "表达清晰流畅，语速适中",
        "内容覆盖全面，包含完整的产品介绍",
        "逻辑结构清晰，有明确的开场和总结",
        "使用了客户案例，增强了说服力"
    ]
    
    # Generate sample improvements
    improvements = [
        "可以增加一些停顿，增强客户的理解和记忆",
        "产品优势的描述可以更加具体",
        "客户痛点的分析可以更加深入",
        "可以增加一些数据支持，增强可信度"
    ]
    
    return {
        "total_score": round(total_score, 1),
        "expression_score": round(scores["expression"], 1),
        "content_score": round(scores["content"], 1),
        "logic_score": round(scores["logic"], 1),
        "customer_score": round(scores["customer"], 1),
        "persuasion_score": round(scores["persuasion"], 1),
        "strengths": strengths,
        "improvements": improvements,
        "transcript": transcript or "这是一段模拟的销售对话...",
        "analysis_date": datetime.now().isoformat()
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Sales Coaching Backend"
    }

# Recording models
class RecordingResponse(BaseModel):
    id: str
    file_name: str
    upload_time: str
    status: str
    score: Optional[float] = None
    file_path: str = ""

class AnalysisRequest(BaseModel):
    recording_id: str

class AnalysisResponse(BaseModel):
    id: str
    file_name: str
    total_score: float
    report: Dict[str, Any]
    status: str

# Upload recording endpoint
@app.post("/api/v1/recordings", response_model=RecordingResponse)
async def upload_recording(file: UploadFile = File(...)):
    """Upload a recording file"""
    try:
        # Generate unique ID
        recording_id = str(uuid.uuid4())
        
        # Validate file type
        valid_types = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/m4a"]
        if file.content_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Supported types: {', '.join(valid_types)}"
            )
        
        # Save file
        file_extension = file.filename.split(".")[-1].lower()
        file_path = os.path.join(UPLOAD_DIR, f"{recording_id}.{file_extension}")
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Store in database
        recordings_db[recording_id] = {
            "id": recording_id,
            "file_name": file.filename,
            "file_path": file_path,
            "upload_time": datetime.now().isoformat(),
            "status": "uploaded",
            "score": None,
            "report": None
        }
        
        return RecordingResponse(
            id=recording_id,
            file_name=file.filename,
            upload_time=datetime.now().isoformat(),
            status="uploaded",
            file_path=file_path
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )

# Get all recordings
@app.get("/api/v1/recordings")
async def get_recordings():
    """Get all recordings"""
    return {
        "recordings": list(recordings_db.values())
    }

# Get recording by ID
@app.get("/api/v1/recordings/{recording_id}")
async def get_recording(recording_id: str):
    """Get a specific recording"""
    if recording_id not in recordings_db:
        raise HTTPException(
            status_code=404,
            detail="Recording not found"
        )
    
    return recordings_db[recording_id]

# Analyze recording endpoint
@app.post("/api/v1/recordings/{recording_id}/analyze")
async def analyze_recording(recording_id: str):
    """Analyze a recording"""
    if recording_id not in recordings_db:
        raise HTTPException(
            status_code=404,
            detail="Recording not found"
        )
    
    # Mock analysis process
    recording = recordings_db[recording_id]
    recording["status"] = "analyzing"
    
    # Simulate processing time
    time.sleep(2)
    
    # Generate report
    report = generate_mock_report()
    recording["status"] = "analyzed"
    recording["score"] = report["total_score"]
    recording["report"] = report
    
    # Save report to file
    report_file = os.path.join(REPORTS_DIR, f"{recording_id}_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return {
        "id": recording_id,
        "file_name": recording["file_name"],
        "total_score": report["total_score"],
        "report": report,
        "status": "analyzed"
    }

# Delete recording endpoint
@app.delete("/api/v1/recordings/{recording_id}")
async def delete_recording(recording_id: str):
    """Delete a recording"""
    if recording_id not in recordings_db:
        raise HTTPException(
            status_code=404,
            detail="Recording not found"
        )
    
    recording = recordings_db[recording_id]
    
    # Remove file
    try:
        if os.path.exists(recording["file_path"]):
            os.remove(recording["file_path"])
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    # Remove report if exists
    try:
        report_file = os.path.join(REPORTS_DIR, f"{recording_id}_report.json")
        if os.path.exists(report_file):
            os.remove(report_file)
    except Exception as e:
        print(f"Error deleting report: {e}")
    
    # Delete from database
    del recordings_db[recording_id]
    
    return {"message": "Recording deleted successfully"}

# API config endpoints
@app.get("/api/v1/api-config")
async def get_api_config():
    """Get API key configuration"""
    return config_db["api_keys"]

@app.post("/api/v1/api-config")
async def update_api_config(config_data: Dict[str, Any]):
    """Update API key configuration"""
    config_db["api_keys"].update(config_data)
    return config_db["api_keys"]

# Scoring config endpoints
@app.get("/api/v1/scoring-config")
async def get_scoring_config():
    """Get scoring configuration"""
    return config_db["scoring_weights"]

@app.post("/api/v1/scoring-config")
async def update_scoring_config(config_data: Dict[str, Any]):
    """Update scoring configuration"""
    config_db["scoring_weights"].update(config_data)
    return config_db["scoring_weights"]

# Static files
@app.get("/api/v1/sample-reports/{report_id}")
async def get_sample_report(report_id: str = "1"):
    """Get sample analysis reports"""
    sample_reports = {
        "1": generate_mock_report(),
        "2": generate_mock_report(),
        "3": generate_mock_report()
    }
    return sample_reports.get(report_id, sample_reports["1"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Sales Coaching Backend Service",
        "version": "2.0.0",
        "endpoints": [
            "/health",
            "/api/v1/recordings",
            "/api/v1/recordings/{id}/analyze",
            "/api/v1/api-config",
            "/api/v1/scoring-config"
        ]
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )