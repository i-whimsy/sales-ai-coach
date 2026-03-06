"""AI Sales Coaching System - Backend API"""

import os
import shutil
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid
import magic
import tempfile

from config import settings
from database import get_db, engine
import models
import speech_analysis
import ai_analyzer

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Sales Coaching System API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
speech_analyzer = speech_analysis.SpeechAnalyzer()

# Directory for uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.VERSION}


@app.post("/api/v1/recordings")
async def upload_recording(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload recording file"""
    try:
        # Validate file type
        file_type = magic.from_buffer(await file.read(), mime=True)
        await file.seek(0)  # Reset file pointer
        
        valid_types = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/m4a"]
        if file_type not in valid_types:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Save file
        file_extension = file.filename.split(".")[-1].lower()
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{file_extension}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create database entry
        recording = models.Recording(
            file_name=file.filename,
            file_path=file_path
        )
        db.add(recording)
        db.commit()
        db.refresh(recording)
        
        return JSONResponse(status_code=201, content={
            "id": recording.id,
            "file_name": recording.file_name,
            "upload_time": recording.upload_time.isoformat(),
            "status": "uploaded"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.post("/api/v1/recordings/{recording_id}/analyze")
async def analyze_recording(recording_id: int, db: Session = Depends(get_db)):
    """Analyze recording"""
    try:
        # Get recording from database
        recording = db.query(models.Recording).filter(
            models.Recording.id == recording_id
        ).first()
        
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Get API key config
        api_config = db.query(models.ApiKeyConfig).first()
        config = {}
        if api_config:
            config = {
                "openai_api_key": api_config.openai_api_key,
                "deepseek_api_key": api_config.deepseek_api_key,
                "claude_api_key": api_config.claude_api_key,
                "whisper_api_key": api_config.whisper_api_key
            }
        
        # Initialize AI analyzer
        ai = ai_analyzer.AIAnalyzer(config)
        
        # Transcribe audio
        transcript, duration = speech_analyzer.transcribe_audio(recording.file_path)
        recording.transcript = transcript
        db.commit()
        
        # Analyze speech characteristics
        speech_result = speech_analyzer.analyze_expression_quality(transcript, duration)
        
        # Analyze with AI
        scoring_config = db.query(models.ScoringConfig).filter(
            models.ScoringConfig.is_active == True
        ).first()
        
        score_weights = None
        if scoring_config:
            score_weights = {
                "expression_weight": scoring_config.expression_weight,
                "content_weight": scoring_config.content_weight,
                "logic_weight": scoring_config.logic_weight,
                "customer_weight": scoring_config.customer_weight,
                "persuasion_weight": scoring_config.persuasion_weight
            }
        
        # Generate report
        report = ai.generate_report(transcript, speech_result, score_weights)
        
        # Save report
        recording.report_json = report
        recording.score = report["total_score"]
        db.commit()
        
        return JSONResponse(status_code=200, content={
            "id": recording.id,
            "file_name": recording.file_name,
            "total_score": report["total_score"],
            "report": report,
            "status": "analyzed"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing recording: {str(e)}")


@app.get("/api/v1/recordings")
async def get_recordings(db: Session = Depends(get_db)):
    """Get all recordings"""
    try:
        recordings = db.query(models.Recording).all()
        result = []
        for recording in recordings:
            item = {
                "id": recording.id,
                "file_name": recording.file_name,
                "upload_time": recording.upload_time.isoformat(),
                "score": recording.score,
                "status": "analyzed" if recording.report_json else "uploaded"
            }
            result.append(item)
        
        return {"recordings": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recordings: {str(e)}")


@app.get("/api/v1/recordings/{recording_id}")
async def get_recording(recording_id: int, db: Session = Depends(get_db)):
    """Get recording by ID"""
    try:
        recording = db.query(models.Recording).filter(
            models.Recording.id == recording_id
        ).first()
        
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        return {
            "id": recording.id,
            "file_name": recording.file_name,
            "upload_time": recording.upload_time.isoformat(),
            "score": recording.score,
            "transcript": recording.transcript,
            "report": recording.report_json,
            "status": "analyzed" if recording.report_json else "uploaded"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recording: {str(e)}")


@app.delete("/api/v1/recordings/{recording_id}")
async def delete_recording(recording_id: int, db: Session = Depends(get_db)):
    """Delete recording"""
    try:
        recording = db.query(models.Recording).filter(
            models.Recording.id == recording_id
        ).first()
        
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Remove file
        if os.path.exists(recording.file_path):
            os.remove(recording.file_path)
        
        # Delete from database
        db.delete(recording)
        db.commit()
        
        return {"message": "Recording deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting recording: {str(e)}")


@app.get("/api/v1/api-config")
async def get_api_config(db: Session = Depends(get_db)):
    """Get API key configuration"""
    try:
        config = db.query(models.ApiKeyConfig).first()
        if config:
            return {
                "openai_api_key": config.openai_api_key,
                "deepseek_api_key": config.deepseek_api_key,
                "claude_api_key": config.claude_api_key,
                "whisper_api_key": config.whisper_api_key
            }
        return {
            "openai_api_key": None,
            "deepseek_api_key": None,
            "claude_api_key": None,
            "whisper_api_key": None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching API config: {str(e)}")


@app.post("/api/v1/api-config")
async def update_api_config(config_data: dict, db: Session = Depends(get_db)):
    """Update API key configuration"""
    try:
        config = db.query(models.ApiKeyConfig).first()
        if not config:
            config = models.ApiKeyConfig()
            db.add(config)
        
        if "openai_api_key" in config_data:
            config.openai_api_key = config_data["openai_api_key"]
        if "deepseek_api_key" in config_data:
            config.deepseek_api_key = config_data["deepseek_api_key"]
        if "claude_api_key" in config_data:
            config.claude_api_key = config_data["claude_api_key"]
        if "whisper_api_key" in config_data:
            config.whisper_api_key = config_data["whisper_api_key"]
        
        db.commit()
        db.refresh(config)
        
        return {
            "openai_api_key": config.openai_api_key,
            "deepseek_api_key": config.deepseek_api_key,
            "claude_api_key": config.claude_api_key,
            "whisper_api_key": config.whisper_api_key
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating API config: {str(e)}")


@app.get("/api/v1/scoring-config")
async def get_scoring_config(db: Session = Depends(get_db)):
    """Get scoring configuration"""
    try:
        config = db.query(models.ScoringConfig).filter(
            models.ScoringConfig.is_active == True
        ).first()
        
        if not config:
            return {
                "expression_weight": 0.20,
                "content_weight": 0.30,
                "logic_weight": 0.20,
                "customer_weight": 0.20,
                "persuasion_weight": 0.10
            }
        
        return {
            "expression_weight": config.expression_weight,
            "content_weight": config.content_weight,
            "logic_weight": config.logic_weight,
            "customer_weight": config.customer_weight,
            "persuasion_weight": config.persuasion_weight
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching scoring config: {str(e)}")


@app.post("/api/v1/scoring-config")
async def update_scoring_config(config_data: dict, db: Session = Depends(get_db)):
    """Update scoring configuration"""
    try:
        config = db.query(models.ScoringConfig).filter(
            models.ScoringConfig.is_active == True
        ).first()
        
        if not config:
            config = models.ScoringConfig(name="Default Scoring")
            db.add(config)
        
        if "expression_weight" in config_data:
            config.expression_weight = config_data["expression_weight"]
        if "content_weight" in config_data:
            config.content_weight = config_data["content_weight"]
        if "logic_weight" in config_data:
            config.logic_weight = config_data["logic_weight"]
        if "customer_weight" in config_data:
            config.customer_weight = config_data["customer_weight"]
        if "persuasion_weight" in config_data:
            config.persuasion_weight = config_data["persuasion_weight"]
        
        db.commit()
        db.refresh(config)
        
        return {
            "expression_weight": config.expression_weight,
            "content_weight": config.content_weight,
            "logic_weight": config.logic_weight,
            "customer_weight": config.customer_weight,
            "persuasion_weight": config.persuasion_weight
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating scoring config: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
