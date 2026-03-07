"""AI Sales Coaching System - Backend API"""

import os
import shutil
import json
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, BackgroundTasks
from fastapi import Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid
import magic
import tempfile
from datetime import datetime

from config import settings
from database import get_db, engine
import models
import speech_analysis
import ai_analyzer
from model_manager import get_model_manager
from models_config import get_model_config

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Sales Coaching System API",
    docs_url=None,
    redoc_url=None
)

# Fix docs for offline usage
from fix_docs import custom_docs
app = custom_docs(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure maximum upload size
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method == "POST":
        content_length = request.headers.get("Content-Length")
        if content_length is not None and int(content_length) > 200 * 1024 * 1024:  # 200MB
            return JSONResponse(
                status_code=413,
                content={"error": "File too large. Maximum file size is 200MB."}
            )
    return await call_next(request)

# Initialize analyzers
speech_analyzer = speech_analysis.SpeechAnalyzer()

# Directory for uploaded files
UPLOAD_DIR = "uploads"
LOGS_DIR = "logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Processing logs storage
processing_logs: Dict[int, List[Dict[str, Any]]] = {}


def log_processing_step(recording_id: int, step: str, status: str = "in_progress", details: str = ""):
    """Log processing steps for real-time updates"""
    if recording_id not in processing_logs:
        processing_logs[recording_id] = []
    
    processing_logs[recording_id].append({
        "step": step,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
    
    # Save to file for persistence
    log_file = os.path.join(LOGS_DIR, f"{recording_id}.log")
    with open(log_file, "a") as f:
        f.write(json.dumps({
            "step": step,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }) + "\n")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.VERSION}


@app.post("/api/v1/recordings")
async def upload_recording(file: UploadFile = File(...), name: str = None, db: Session = Depends(get_db)):
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
            name=name,
            file_name=file.filename,
            file_path=file_path
        )
        db.add(recording)
        db.commit()
        db.refresh(recording)
        
        return JSONResponse(status_code=201, content={
            "id": recording.id,
            "name": recording.name,
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
        
        # Clear existing logs
        if recording_id in processing_logs:
            del processing_logs[recording_id]
        
        log_processing_step(recording_id, "分析任务开始", "in_progress", "开始处理录音文件")
        
        # Get API key config
        log_processing_step(recording_id, "加载配置", "in_progress", "获取API密钥配置")
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
        log_processing_step(recording_id, "初始化分析器", "in_progress", "加载AI分析组件")
        ai = ai_analyzer.AIAnalyzer(config)
        
        # Transcribe audio
        log_processing_step(recording_id, "语音转文本", "in_progress", "使用Whisper Base模型进行转录")
        transcript, duration = speech_analyzer.transcribe_audio(recording.file_path)
        recording.transcript = transcript
        db.commit()
        log_processing_step(recording_id, "语音转文本", "completed", f"成功转录{len(transcript.split())}个单词")
        
        # Analyze speech characteristics
        log_processing_step(recording_id, "表达质量分析", "in_progress", "分析语速、停顿、流畅度等指标")
        speech_result = speech_analyzer.analyze_expression_quality(transcript, duration)
        log_processing_step(recording_id, "表达质量分析", "completed", f"表达得分: {speech_result['expression_score']}")
        
        # Analyze with AI
        log_processing_step(recording_id, "内容分析", "in_progress", "分析内容完整性、逻辑结构等")
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
        log_processing_step(recording_id, "生成报告", "in_progress", "综合所有指标生成最终报告")
        report = ai.generate_report(transcript, speech_result, score_weights)
        
        # Save report
        recording.report_json = report
        recording.score = report["total_score"]
        db.commit()
        
        log_processing_step(recording_id, "分析完成", "completed", f"最终得分: {report['total_score']}")
        
        return JSONResponse(status_code=200, content={
            "id": recording.id,
            "file_name": recording.file_name,
            "total_score": report["total_score"],
            "report": report,
            "status": "analyzed",
            "transcript": transcript,
            "stt_model": "Whisper Base (本地模型)",
            "processing_steps": processing_logs.get(recording_id, [])
        })
    
    except Exception as e:
        log_processing_step(recording_id, "分析失败", "failed", str(e))
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
                "name": recording.name,
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
            "name": recording.name,
            "file_name": recording.file_name,
            "upload_time": recording.upload_time.isoformat(),
            "score": recording.score,
            "transcript": recording.transcript,
            "report": recording.report_json,
            "status": "analyzed" if recording.report_json else "uploaded"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recording: {str(e)}")


@app.get("/api/v1/recordings/{recording_id}/transcript")
async def get_transcript(recording_id: int, db: Session = Depends(get_db)):
    """Get transcript text for download"""
    try:
        recording = db.query(models.Recording).filter(
            models.Recording.id == recording_id
        ).first()
        
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        if not recording.transcript:
            raise HTTPException(status_code=404, detail="Transcript not available")
        
        # Create temporary file for download
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write(recording.transcript)
        temp_file.close()
        
        return FileResponse(
            path=temp_file.name,
            filename=f"transcript_{recording_id}.txt",
            media_type="text/plain"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting transcript: {str(e)}")


@app.get("/api/v1/recordings/{recording_id}/logs")
async def get_processing_logs(recording_id: int):
    """Get real-time processing logs"""
    return {"logs": processing_logs.get(recording_id, [])}


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
        
        # Remove log file
        log_file = os.path.join(LOGS_DIR, f"{recording_id}.log")
        if os.path.exists(log_file):
            os.remove(log_file)
        
        # Remove from processing logs
        if recording_id in processing_logs:
            del processing_logs[recording_id]
        
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


def compare_recordings(recording1, recording2):
    """Compare two recordings and return detailed comparison results"""
    try:
        # Basic comparison
        comparison = {
            "summary": {
                "recording1": {
                    "id": recording1.id,
                    "name": recording1.name or recording1.file_name,
                    "score": recording1.score,
                    "score_formatted": f"{recording1.score:.1f}" if recording1.score is not None else "--"
                },
                "recording2": {
                    "id": recording2.id,
                    "name": recording2.name or recording2.file_name,
                    "score": recording2.score,
                    "score_formatted": f"{recording2.score:.1f}" if recording2.score is not None else "--"
                },
                "better_performer": "recording1" if recording1.score and recording2.score and recording1.score > recording2.score else "recording2" if recording2.score is not None else None
            },
            "dimension_comparison": {},
            "key_points_comparison": [],
            "summary_analysis": []
        }

        # Compare dimension scores if reports exist
        if recording1.report_json and recording2.report_json:
            dim1 = recording1.report_json.get('dimension_scores', {})
            dim2 = recording2.report_json.get('dimension_scores', {})
            
            for dimension in ['expression', 'content', 'logic', 'customer_understanding', 'persuasion']:
                score1 = dim1.get(dimension)
                score2 = dim2.get(dimension)
                
                if score1 is not None and score2 is not None:
                    comparison["dimension_comparison"][dimension] = {
                        "recording1": score1,
                        "recording2": score2,
                        "difference": score1 - score2,
                        "better": "recording1" if score1 > score2 else "recording2"
                    }

            # Extract key points from transcripts
            if recording1.transcript and recording2.transcript:
                comparison["key_points_comparison"] = analyze_key_points(recording1.transcript, recording2.transcript)

            # Generate summary analysis
            if recording1.score and recording2.score:
                diff = recording1.score - recording2.score
                comparison["summary_analysis"] = generate_summary_analysis(
                    recording1, recording2, diff, comparison["summary_analysis"]
                )

        return comparison
    except Exception as e:
        print(f"Error comparing recordings: {str(e)}")
        return {"error": f"Comparison failed: {str(e)}"}


def analyze_key_points(transcript1, transcript2):
    """Analyze and compare key points from transcripts"""
    # Extract keywords (simplified approach)
    keywords1 = extract_keywords(transcript1)
    keywords2 = extract_keywords(transcript2)
    
    # Find common keywords and unique keywords
    common_keywords = list(set(keywords1) & set(keywords2))
    unique_to_1 = list(set(keywords1) - set(keywords2))
    unique_to_2 = list(set(keywords2) - set(keywords1))
    
    return {
        "common_topics": common_keywords[:10],
        "unique_to_recording1": unique_to_1[:10],
        "unique_to_recording2": unique_to_2[:10],
        "coverage_analysis": {
            "common_topics_count": len(common_keywords),
            "unique_to_recording1_count": len(unique_to_1),
            "unique_to_recording2_count": len(unique_to_2)
        }
    }


def extract_keywords(text):
    """Extract keywords from text (simplified approach)"""
    # Remove punctuation and lowercase
    text = text.lower()
    text = text.replace('，', '').replace('。', '').replace('？', '').replace('！', '')
    text = text.replace(',', '').replace('.', '').replace('?', '').replace('!', '')
    
    # Simple keyword extraction by splitting and filtering stopwords
    words = text.split()
    stopwords = set(['的', '了', '是', '和', '在', '我', '有', '就', '都', '要', '对', '这', '那', '也', '而', '但', '我们', '你们', '他们'])
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    
    # Count word frequency and get top keywords
    word_counts = {}
    for word in filtered_words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words]


def generate_summary_analysis(recording1, recording2, diff, existing_analysis):
    """Generate summary analysis based on comparison"""
    analysis = existing_analysis.copy()
    
    if diff > 5:
        analysis.append(f"录音1比录音2表现优秀得多，总分高出{diff:.1f}分")
    elif diff > 2:
        analysis.append(f"录音1比录音2表现更好，总分高出{diff:.1f}分")
    elif diff < -5:
        analysis.append(f"录音2比录音1表现优秀得多，总分高出{-diff:.1f}分")
    elif diff < -2:
        analysis.append(f"录音2比录音1表现更好，总分高出{-diff:.1f}分")
    else:
        analysis.append("两个录音的表现相当")
    
    # Compare dimension scores if available
    if recording1.report_json and recording2.report_json:
        dim1 = recording1.report_json.get('dimension_scores', {})
        dim2 = recording2.report_json.get('dimension_scores', {})
        
        for dimension, name in [
            ('expression', '表达质量'),
            ('content', '内容完整度'),
            ('logic', '逻辑结构'),
            ('customer_understanding', '客户理解度'),
            ('persuasion', '说服力')
        ]:
            score1 = dim1.get(dimension)
            score2 = dim2.get(dimension)
            if score1 is not None and score2 is not None:
                dim_diff = score1 - score2
                if abs(dim_diff) > 10:
                    if dim_diff > 0:
                        analysis.append(f"在{name}维度，录音1表现明显优于录音2（{score1:.1f} vs {score2:.1f}")
                    else:
                        analysis.append(f"在{name}维度，录音2表现明显优于录音1（{score2:.1f} vs {score1:.1f}")
    
    return analysis


@app.post("/api/v1/comparison")
async def create_comparison(recording_ids: List[int], name: str, db: Session = Depends(get_db)):
    """Create comparison between two recordings"""
    try:
        if len(recording_ids) != 2:
            raise HTTPException(status_code=400, detail="Please provide exactly two recording IDs")
        
        recording1 = db.query(models.Recording).get(recording_ids[0])
        recording2 = db.query(models.Recording).get(recording_ids[1])
        
        if not recording1:
            raise HTTPException(status_code=404, detail=f"Recording {recording_ids[0]} not found")
        if not recording2:
            raise HTTPException(status_code=404, detail=f"Recording {recording_ids[1]} not found")
        
        # Create comparison entry
        comparison_result = compare_recordings(recording1, recording2)
        
        # Create database entry
        comparison = models.Comparison(
            name=name,
            recording1_id=recording1.id,
            recording2_id=recording2.id,
            comparison_result=comparison_result
        )
        
        db.add(comparison)
        db.commit()
        db.refresh(comparison)
        
        return JSONResponse(status_code=201, content={
            "id": comparison.id,
            "name": comparison.name,
            "recording_ids": recording_ids,
            "comparison": comparison_result,
            "created_at": comparison.created_at.isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating comparison: {str(e)}")


@app.get("/api/v1/comparison/{comparison_id}")
async def get_comparison(comparison_id: int, db: Session = Depends(get_db)):
    """Get comparison results by ID"""
    try:
        comparison = db.query(models.Comparison).get(comparison_id)
        
        if not comparison:
            raise HTTPException(status_code=404, detail="Comparison not found")
        
        return {
            "id": comparison.id,
            "name": comparison.name,
            "recording1_id": comparison.recording1_id,
            "recording2_id": comparison.recording2_id,
            "comparison": comparison.comparison_result,
            "created_at": comparison.created_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting comparison: {str(e)}")


@app.get("/api/v1/comparison")
async def get_all_comparisons(db: Session = Depends(get_db)):
    """Get all comparisons"""
    try:
        comparisons = db.query(models.Comparison).all()
        result = []
        
        for comparison in comparisons:
            result.append({
                "id": comparison.id,
                "name": comparison.name,
                "recording1_id": comparison.recording1_id,
                "recording2_id": comparison.recording2_id,
                "created_at": comparison.created_at.isoformat()
            })
        
        return {"comparisons": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting comparisons: {str(e)}")


@app.delete("/api/v1/comparison/{comparison_id}")
async def delete_comparison(comparison_id: int, db: Session = Depends(get_db)):
    """Delete comparison"""
    try:
        comparison = db.query(models.Comparison).get(comparison_id)
        
        if not comparison:
            raise HTTPException(status_code=404, detail="Comparison not found")
        
        db.delete(comparison)
        db.commit()
        
        return {"message": "Comparison deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting comparison: {str(e)}")


@app.post("/api/v1/recordings/{recording_id}/rename")
async def rename_recording(recording_id: int, name_data: Dict[str, str], db: Session = Depends(get_db)):
    """Rename a recording"""
    try:
        recording = db.query(models.Recording).get(recording_id)
        
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        recording.name = name_data.get('name')
        db.commit()
        db.refresh(recording)
        
        return {
            "id": recording.id,
            "name": recording.name,
            "file_name": recording.file_name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error renaming recording: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ========== 模型管理API ==========

@app.get("/api/v1/models")
async def list_models(
    scene: str = "speech_analysis",
    task_type: str = "asr",
    db: Session = Depends(get_db)
):
    """获取可用模型列表"""
    # 获取API配置
    api_config = get_api_config_dict(db)
    model_manager = get_model_manager(api_config)
    
    models = model_manager.get_models_for_ui(scene=scene, task_type=task_type)
    
    # 获取用户偏好
    preference = db.query(models.ModelPreference).filter(
        models.ModelPreference.scene == scene,
        models.ModelPreference.task_type == task_type,
        models.ModelPreference.is_active == True
    ).first()
    
    return {
        "models": models,
        "selected_model_id": preference.selected_model_id if preference else None
    }


@app.get("/api/v1/models/all")
async def list_all_models():
    """获取所有模型配置（用于管理）"""
    from models_config import get_all_models
    all_models = get_all_models()
    return {
        "models": [model.to_dict() for model in all_models]
    }


@app.post("/api/v1/models/preference")
async def set_model_preference(
    scene: str,
    task_type: str,
    model_id: str,
    db: Session = Depends(get_db)
):
    """设置模型偏好"""
    # 验证模型存在
    model_config = get_model_config(model_id)
    if not model_config:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
    
    # 停用现有偏好
    existing = db.query(models.ModelPreference).filter(
        models.ModelPreference.scene == scene,
        models.ModelPreference.task_type == task_type
    ).all()
    for pref in existing:
        pref.is_active = False
    
    # 创建新偏好
    preference = models.ModelPreference(
        scene=scene,
        task_type=task_type,
        selected_model_id=model_id,
        is_active=True
    )
    
    db.add(preference)
    db.commit()
    db.refresh(preference)
    
    return {"success": True, "preference": {
        "scene": preference.scene,
        "task_type": preference.task_type,
        "selected_model_id": preference.selected_model_id
    }}


@app.get("/api/v1/models/preference")
async def get_model_preference(
    scene: str,
    task_type: str,
    db: Session = Depends(get_db)
):
    """获取模型偏好"""
    preference = db.query(models.ModelPreference).filter(
        models.ModelPreference.scene == scene,
        models.ModelPreference.task_type == task_type,
        models.ModelPreference.is_active == True
    ).first()
    
    if preference:
        return {
            "scene": preference.scene,
            "task_type": preference.task_type,
            "selected_model_id": preference.selected_model_id
        }
    else:
        return {
            "scene": scene,
            "task_type": task_type,
            "selected_model_id": None
        }


def get_api_config_dict(db: Session) -> Dict[str, str]:
    """获取API配置字典"""
    api_config = db.query(models.ApiKeyConfig).first()
    config_dict = {}
    if api_config:
        if api_config.openai_api_key:
            config_dict["openai_api_key"] = api_config.openai_api_key
        if api_config.deepseek_api_key:
            config_dict["deepseek_api_key"] = api_config.deepseek_api_key
        if api_config.claude_api_key:
            config_dict["claude_api_key"] = api_config.claude_api_key
        if api_config.whisper_api_key:
            config_dict["whisper_api_key"] = api_config.whisper_api_key
    return config_dict
