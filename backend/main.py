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
from model_installer import ModelInstaller

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

# Fix docs for offline usage (暂时移除，直到找到fix_docs模块)
# from fix_docs import custom_docs
# app = custom_docs(app)

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
async def upload_recording(
    file: UploadFile = File(...), 
    name: str = None, 
    model_id: int = None,
    db: Session = Depends(get_db)
):
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
        
        # Validate model_id if provided
        selected_model = None
        if model_id:
            selected_model = db.query(models.AIModel).filter(
                models.AIModel.id == model_id,
                models.AIModel.status == "active"
            ).first()
            if not selected_model:
                raise HTTPException(status_code=400, detail="无效的模型ID或模型未激活")
        
        # Create database entry
        recording = models.Recording(
            name=name,
            file_name=file.filename,
            file_path=file_path,
            model_id=model_id  # 保存选择的模型ID
        )
        db.add(recording)
        db.commit()
        db.refresh(recording)
        
        return JSONResponse(status_code=201, content={
            "id": recording.id,
            "name": recording.name,
            "file_name": recording.file_name,
            "upload_time": recording.upload_time.isoformat(),
            "status": "uploaded",
            "model_id": recording.model_id,
            "model_name": selected_model.name if selected_model else None
        })
    
    except HTTPException:
        raise
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
        
        # Get selected model for this recording
        selected_model = None
        if recording.model_id:
            selected_model = db.query(models.AIModel).filter(
                models.AIModel.id == recording.model_id,
                models.AIModel.status == "active"
            ).first()
        
        model_info = "默认Whisper模型"
        if selected_model:
            model_info = f"{selected_model.name} ({selected_model.type})"
            # Update config with model's API key if available
            if selected_model.api_key:
                config["whisper_api_key"] = selected_model.api_key
            if selected_model.type == "online" and selected_model.model_name:
                config["whisper_model"] = selected_model.model_name
        
        # Initialize AI analyzer
        log_processing_step(recording_id, "初始化分析器", "in_progress", "加载AI分析组件")
        ai = ai_analyzer.AIAnalyzer(config)
        
        # Transcribe audio
        log_processing_step(recording_id, "语音转文本", "in_progress", f"使用{model_info}进行转录")
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
        
        # Save report - convert dict to JSON string
        import json
        recording.report_json = json.dumps(report, ensure_ascii=False)
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
            # Get model info
            model_name = None
            if recording.model_id:
                model = db.query(models.AIModel).filter(models.AIModel.id == recording.model_id).first()
                if model:
                    model_name = model.name
            
            item = {
                "id": recording.id,
                "name": recording.name,
                "file_name": recording.file_name,
                "upload_time": recording.upload_time.isoformat() + "Z",  # 添加Z表示UTC时间
                "score": recording.score,
                "status": "analyzed" if recording.report_json else "uploaded",
                "model_id": recording.model_id,
                "model_name": model_name
            }
            result.append(item)
        
        return {"recordings": result}
    
    except Exception as e:
        print(f"Error fetching recordings: {str(e)}")  # 添加日志以便调试
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
        
        # Get model info if available
        model_name = None
        if recording.model_id:
            model = db.query(models.AIModel).filter(models.AIModel.id == recording.model_id).first()
            if model:
                model_name = model.name
        
        return {
            "id": recording.id,
            "name": recording.name,
            "file_name": recording.file_name,
            "upload_time": recording.upload_time.isoformat(),
            "score": recording.score,
            "transcript": recording.transcript,
            "report": recording.report_json,
            "status": "analyzed" if recording.report_json else "uploaded",
            "model_id": recording.model_id,
            "model_name": model_name
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


# ========== 模型管理API ==========

@app.get("/api/v1/models")
async def get_models(
    category: str = None,
    type: str = None,
    scene: str = None,
    task_type: str = None,
    db: Session = Depends(get_db)
):
    """获取所有模型列表
    
    支持按分类、类型、场景和任务类型筛选
    - scene: 场景名称，如 "speech_analysis"
    - task_type: 任务类型，如 "asr", "nlp", "emotion" 等
    """
    query = db.query(models.AIModel)
    
    if category:
        query = query.filter(models.AIModel.category == category)
    if type:
        query = query.filter(models.AIModel.type == type)
    
    models_list = query.all()
    
    # 如果指定了scene和task_type，获取用户偏好的模型
    selected_model_id = None
    if scene and task_type:
        preference = db.query(models.ModelPreference).filter(
            models.ModelPreference.scene == scene,
            models.ModelPreference.task_type == task_type,
            models.ModelPreference.is_active == True
        ).first()
        if preference:
            selected_model_id = preference.selected_model_id
    
    result = []
    for model in models_list:
        # 获取模型标签
        tags = db.query(models.ModelTag).join(
            models.ModelTagRelation,
            models.ModelTag.id == models.ModelTagRelation.tag_id
        ).filter(
            models.ModelTagRelation.model_id == model.id
        ).all()
        
        tag_list = [{"id": t.id, "name": t.name, "color": t.color} for t in tags]
        
        result.append({
            "id": model.id,
            "name": model.name,
            "type": model.type,
            "category": model.category,
            "provider": model.provider,
            "api_url": model.api_url,
            "model_name": model.model_name,
            "local_path": model.local_path,
            "status": model.status,
            "is_default": model.is_default,
            "selected": model.id == selected_model_id,
            "tags": tag_list,
            "created_at": model.created_at.isoformat() + "Z" if model.created_at else None,
            "updated_at": model.updated_at.isoformat() + "Z" if model.updated_at else None
        })
    
    return {"models": result, "selected_model_id": selected_model_id}


@app.post("/api/v1/models")
async def create_model(model_data: dict, db: Session = Depends(get_db)):
    """创建新模型"""
    try:
        # 验证必填字段
        required_fields = ["name", "type", "category", "provider"]
        for field in required_fields:
            if field not in model_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # 创建模型
        model = models.AIModel(
            name=model_data["name"],
            type=model_data["type"],
            category=model_data["category"],
            provider=model_data["provider"],
            api_url=model_data.get("api_url"),
            api_key=model_data.get("api_key"),
            model_name=model_data.get("model_name"),
            local_path=model_data.get("local_path"),
            config=model_data.get("config"),
            is_default=model_data.get("is_default", False)
        )
        
        # 如果是默认模型，取消其他同分类的默认
        if model.is_default:
            db.query(models.AIModel).filter(
                models.AIModel.category == model.category
            ).update({"is_default": False})
        
        db.add(model)
        db.commit()
        db.refresh(model)
        
        return JSONResponse(status_code=201, content={
            "id": model.id,
            "name": model.name,
            "type": model.type,
            "category": model.category,
            "provider": model.provider,
            "status": model.status,
            "is_default": model.is_default
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating model: {str(e)}")


@app.get("/api/v1/models/{model_id}")
async def get_model(model_id: int, db: Session = Depends(get_db)):
    """获取模型详情"""
    model = db.query(models.AIModel).get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return {
        "id": model.id,
        "name": model.name,
        "type": model.type,
        "category": model.category,
        "provider": model.provider,
        "api_url": model.api_url,
        "api_key": model.api_key,
        "model_name": model.model_name,
        "local_path": model.local_path,
        "status": model.status,
        "is_default": model.is_default,
        "config": model.config,
        "created_at": model.created_at.isoformat() + "Z",
        "updated_at": model.updated_at.isoformat() + "Z"
    }


@app.put("/api/v1/models/{model_id}")
async def update_model(model_id: int, model_data: dict, db: Session = Depends(get_db)):
    """更新模型配置"""
    model = db.query(models.AIModel).get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # 更新字段
        if "name" in model_data:
            model.name = model_data["name"]
        if "type" in model_data:
            model.type = model_data["type"]
        if "category" in model_data:
            model.category = model_data["category"]
        if "provider" in model_data:
            model.provider = model_data["provider"]
        if "api_url" in model_data:
            model.api_url = model_data["api_url"]
        if "api_key" in model_data:
            model.api_key = model_data["api_key"]
        if "model_name" in model_data:
            model.model_name = model_data["model_name"]
        if "local_path" in model_data:
            model.local_path = model_data["local_path"]
        if "config" in model_data:
            model.config = model_data["config"]
        
        # 处理默认设置
        if "is_default" in model_data:
            if model_data["is_default"]:
                # 取消其他同分类的默认
                db.query(models.AIModel).filter(
                    models.AIModel.category == model.category,
                    models.AIModel.id != model_id
                ).update({"is_default": False})
            model.is_default = model_data["is_default"]
        
        db.commit()
        db.refresh(model)
        
        return {
            "id": model.id,
            "name": model.name,
            "type": model.type,
            "category": model.category,
            "provider": model.provider,
            "status": model.status,
            "is_default": model.is_default
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating model: {str(e)}")


@app.delete("/api/v1/models/{model_id}")
async def delete_model(model_id: int, db: Session = Depends(get_db)):
    """删除模型"""
    model = db.query(models.AIModel).get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        db.delete(model)
        db.commit()
        return {"message": "Model deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting model: {str(e)}")


@app.post("/api/v1/models/{model_id}/test")
async def test_model(model_id: int, db: Session = Depends(get_db)):
    """测试模型可用性"""
    model = db.query(models.AIModel).get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        if model.type == "online":
            # 测试在线模型
            if not model.api_url or not model.api_key:
                raise Exception("API URL or API Key not configured")
            
            # 简单的连接测试
            import requests
            headers = {"Authorization": f"Bearer {model.api_key}"}
            response = requests.get(model.api_url + "/health", headers=headers, timeout=5)
            response.raise_for_status()
            
            model.status = "active"
            
        elif model.type == "local":
            # 测试本地模型
            if not model.local_path or not os.path.exists(model.local_path):
                raise Exception("Local model path not exists")
            
            # 测试模型加载
            # 这里可以添加实际的模型加载测试
            model.status = "active"
        
        db.commit()
        
        return {
            "success": True,
            "status": model.status,
            "message": "Model test passed"
        }
        
    except Exception as e:
        model.status = "error"
        db.commit()
        
        return {
            "success": False,
            "status": model.status,
            "message": f"Model test failed: {str(e)}"
        }


@app.post("/api/v1/models/call")
async def call_unified_model(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    统一模型调用接口
    根据任务名称自动选择合适的模型，或指定特定模型
    """
    try:
        data = await request.json()
        
        task_name = data.get("task_name")
        input_data = data.get("input_data", {})
        model_id = data.get("model_id")
        
        if not task_name:
            raise HTTPException(status_code=400, detail="task_name 是必填字段")
        
        from model_manager import ModelManager
        
        manager = ModelManager(db)
        
        print(f"Received call for task: {task_name}")
        
        if model_id:
            print(f"Calling specific model: {model_id}")
            # 调用指定模型
            model = db.query(models.AIModel).filter(
                models.AIModel.id == model_id,
                models.AIModel.status == "active"
            ).first()
            
            if not model:
                raise HTTPException(status_code=400, detail=f"模型 {model_id} 不可用")
            
            result = await manager._call_specific_model(model, input_data)
            return {
                "success": True,
                "model_id": model.id,
                "model_name": model.name,
                "result": result
            }
        else:
            print(f"Calling task model for task: {task_name}")
            # 自动选择模型
            
            # First, get task configuration
            task_config = db.query(models.TaskModelConfig).filter(
                models.TaskModelConfig.task_name == task_name,
                models.TaskModelConfig.is_active == True
            ).first()
            
            if not task_config:
                raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 未配置")
            
            print(f"Task config found: {task_config}")
            print(f"Task required tags: {task_config.required_tags}")
            
            candidate_models = []
            
            # 获取用户偏好模型
            preference = db.query(models.ModelPreference).filter(
                models.ModelPreference.task_type == task_name,
                models.ModelPreference.is_active == True
            ).first()
            
            print(f"User preference found: {preference}")
            
            # 优先使用用户选择的模型
            if preference and preference.selected_model_id:
                user_model = db.query(models.AIModel).filter(
                    models.AIModel.id == preference.selected_model_id,
                    models.AIModel.status == "active"
                ).first()
                
                if user_model:
                    print(f"Adding user selected model: {user_model.name}")
                    candidate_models.append(user_model)
            
            # 添加任务默认模型
            if task_config.default_model_id:
                default_model = db.query(models.AIModel).filter(
                    models.AIModel.id == task_config.default_model_id,
                    models.AIModel.status == "active"
                ).first()
                
                if default_model:
                    print(f"Adding default model: {default_model.name}")
                    candidate_models.append(default_model)
            
            # 添加备选模型
            if task_config.fallback_model_ids:
                for model_id in task_config.fallback_model_ids:
                    fallback_model = db.query(models.AIModel).filter(
                        models.AIModel.id == model_id,
                        models.AIModel.status == "active"
                    ).first()
                    
                    if fallback_model:
                        print(f"Adding fallback model: {fallback_model.name}")
                        candidate_models.append(fallback_model)
            
            # 如果没有候选模型，获取符合标签要求的所有可用模型
            if not candidate_models:
                print("No configured models found, searching by tags")
                candidate_models = manager.get_models_for_task(task_name)
                
                print(f"Found {len(candidate_models)} tag-matching models")
                for model in candidate_models:
                    print(f"  - {model.name} (ID: {model.id})")
            
            if not candidate_models:
                raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 没有可用的模型")
            
            # 依次尝试调用模型
            last_error = None
            for model in candidate_models:
                try:
                    print(f"Calling model: {model.name}")
                    result = await manager._call_specific_model(model, input_data)
                    return {
                        "success": True,
                        "model_id": model.id,
                        "model_name": model.name,
                        "result": result
                    }
                except Exception as e:
                    last_error = e
                    print(f"Model call failed: {str(e)}")
                    continue
            
            raise HTTPException(status_code=500, detail=f"所有模型调用失败: {str(last_error)}")
            
    except Exception as e:
        print(f"Error in call_unified_model: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"模型调用失败: {str(e)}")


@app.get("/api/v1/models/categories")
async def get_model_categories():
    """获取模型分类列表"""
    categories = [
        {"id": "ASR", "name": "语音识别", "description": "将语音转换为文本"},
        {"id": "NLP", "name": "自然语言处理", "description": "文本分析、理解、生成"},
        {"id": "EMOTION", "name": "情感分析", "description": "分析语音/文本情感倾向"},
        {"id": "VOICEPRINT", "name": "声纹识别", "description": "说话人身份识别"},
        {"id": "INTENT", "name": "意图识别", "description": "识别说话人的意图"},
        {"id": "SCORE", "name": "评分模型", "description": "对销售话术进行评分"}
    ]
    return {"categories": categories}


@app.get("/api/v1/models/defaults")
async def get_default_models(db: Session = Depends(get_db)):
    """获取各分类默认模型"""
    default_models = db.query(models.AIModel).filter(
        models.AIModel.is_default == True
    ).all()
    
    result = {}
    for model in default_models:
        result[model.category] = {
            "id": model.id,
            "name": model.name,
            "type": model.type,
            "provider": model.provider
        }
    
    return {"default_models": result}


@app.get("/api/v1/models/local/installed")
async def get_installed_local_models():
    """获取已安装的本地模型列表"""
    try:
        models = ModelInstaller.list_installed_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching installed models: {str(e)}")


@app.post("/api/v1/models/local/install/{model_name}")
async def install_local_model(model_name: str):
    """安装本地模型"""
    try:
        result = ModelInstaller.install_whisper_model(model_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error installing model: {str(e)}")


@app.delete("/api/v1/models/local/uninstall/{model_name}")
async def uninstall_local_model(model_name: str):
    """卸载本地模型"""
    try:
        result = ModelInstaller.uninstall_whisper_model(model_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uninstalling model: {str(e)}")


@app.post("/api/v1/models/local/check/{model_name}")
async def check_local_model(model_name: str):
    """检查本地模型可用性"""
    try:
        result = ModelInstaller.check_model_availability(model_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking model: {str(e)}")


# 初始化默认模型
@app.on_event("startup")
async def init_default_models():
    """系统启动时初始化默认模型"""
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        # 检查是否已有模型
        existing = db.query(models.AIModel).count()
        if existing > 0:
            return
        
        # 初始化默认在线模型
        default_models = [
            # ASR 模型
            {
                "name": "OpenAI Whisper API",
                "type": "online",
                "category": "ASR",
                "provider": "OpenAI",
                "api_url": "https://api.openai.com/v1/audio/transcriptions",
                "model_name": "whisper-1",
                "is_default": True
            },
            {
                "name": "字节跳动火山引擎Whisper",
                "type": "online",
                "category": "ASR",
                "provider": "字节跳动",
                "api_url": "https://ark.cn-beijing.volces.com/api/v3/audio/transcriptions",
                "model_name": "whisper-large-v3",
                "is_default": False
            },
            {
                "name": "DeepSeek 语音识别",
                "type": "online",
                "category": "ASR",
                "provider": "DeepSeek",
                "api_url": "https://api.deepseek.com/v1/audio/transcriptions",
                "model_name": "whisper-1",
                "is_default": False
            },
            
            # NLP 模型
            {
                "name": "OpenAI GPT-4o",
                "type": "online",
                "category": "NLP",
                "provider": "OpenAI",
                "api_url": "https://api.openai.com/v1/chat/completions",
                "model_name": "gpt-4o",
                "is_default": True
            },
            {
                "name": "字节跳动豆包4",
                "type": "online",
                "category": "NLP",
                "provider": "字节跳动",
                "api_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                "model_name": "doubao-4-pro-250515",
                "is_default": False
            },
            {
                "name": "DeepSeek V3",
                "type": "online",
                "category": "NLP",
                "provider": "DeepSeek",
                "api_url": "https://api.deepseek.com/v1/chat/completions",
                "model_name": "deepseek-chat",
                "is_default": False
            },
            
            # 本地模型
            {
                "name": "本地 Whisper Base",
                "type": "local",
                "category": "ASR",
                "provider": "OpenAI",
                "local_path": "~/.cache/whisper/base.pt",
                "model_name": "base",
                "is_default": False
            },
            {
                "name": "本地 Whisper Small",
                "type": "local",
                "category": "ASR",
                "provider": "OpenAI",
                "local_path": "~/.cache/whisper/small.pt",
                "model_name": "small",
                "is_default": False
            }
        ]
        
        for model_data in default_models:
            model = models.AIModel(**model_data)
            db.add(model)
        
        db.commit()
        print("✅ Default models initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing default models: {str(e)}")
    finally:
        db.close()


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


# ========== 任务模型配置API ==========

@app.get("/api/v1/tasks")
async def get_tasks(
    include_models: bool = False,
    db: Session = Depends(get_db)
):
    """获取所有任务配置列表"""
    tasks = db.query(models.TaskModelConfig).filter(
        models.TaskModelConfig.is_active == True
    ).all()
    
    result = []
    for task in tasks:
        task_dict = {
            "task_name": task.task_name,
            "description": task.description,
            "required_tags": task.required_tags,
            "default_model_id": task.default_model_id,
            "fallback_model_ids": task.fallback_model_ids or [],
            "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
            "updated_at": task.updated_at.isoformat() + "Z" if task.updated_at else None
        }
        
        if include_models and task.default_model_id:
            default_model = db.query(models.AIModel).filter(
                models.AIModel.id == task.default_model_id
            ).first()
            if default_model:
                task_dict["default_model"] = {
                    "id": default_model.id,
                    "name": default_model.name
                }
        
        result.append(task_dict)
    
    return {"tasks": result}


@app.get("/api/v1/tasks/{task_name}")
async def get_task_config(
    task_name: str,
    include_models: bool = False,
    db: Session = Depends(get_db)
):
    """获取特定任务的配置"""
    task = db.query(models.TaskModelConfig).filter(
        models.TaskModelConfig.task_name == task_name,
        models.TaskModelConfig.is_active == True
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"任务 {task_name} 未找到")
    
    result = {
        "task_name": task.task_name,
        "description": task.description,
        "required_tags": task.required_tags,
        "default_model_id": task.default_model_id,
        "fallback_model_ids": task.fallback_model_ids or [],
        "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
        "updated_at": task.updated_at.isoformat() + "Z" if task.updated_at else None
    }
    
    if include_models and task.default_model_id:
        default_model = db.query(models.AIModel).filter(
            models.AIModel.id == task.default_model_id
        ).first()
        if default_model:
            result["default_model"] = {
                "id": default_model.id,
                "name": default_model.name
            }
    
    return result


@app.put("/api/v1/tasks/{task_name}")
async def update_task_config(
    task_name: str,
    config_data: dict,
    db: Session = Depends(get_db)
):
    """更新任务配置"""
    task = db.query(models.TaskModelConfig).filter(
        models.TaskModelConfig.task_name == task_name
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"任务 {task_name} 未找到")
    
    # 更新配置字段
    if "description" in config_data:
        task.description = config_data["description"]
    if "required_tags" in config_data:
        task.required_tags = config_data["required_tags"]
    if "default_model_id" in config_data:
        # 验证模型ID是否有效
        if config_data["default_model_id"]:
            model = db.query(models.AIModel).filter(
                models.AIModel.id == config_data["default_model_id"]
            ).first()
            if not model:
                raise HTTPException(status_code=400, detail="无效的模型ID")
        task.default_model_id = config_data["default_model_id"]
    if "fallback_model_ids" in config_data:
        # 验证所有备选模型ID是否有效
        for model_id in config_data["fallback_model_ids"]:
            model = db.query(models.AIModel).filter(
                models.AIModel.id == model_id
            ).first()
            if not model:
                raise HTTPException(status_code=400, detail=f"无效的模型ID: {model_id}")
        task.fallback_model_ids = config_data["fallback_model_ids"]
    
    task.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"任务 {task_name} 配置已更新"}


# ========== 模型标签API ==========

@app.get("/api/v1/tags")
async def get_tags(
    db: Session = Depends(get_db)
):
    """获取所有模型标签"""
    tags = db.query(models.ModelTag).all()
    
    result = []
    for tag in tags:
        result.append({
            "id": tag.id,
            "name": tag.name,
            "description": tag.description,
            "color": tag.color,
            "created_at": tag.created_at.isoformat() + "Z" if tag.created_at else None
        })
    
    return {"tags": result}


@app.post("/api/v1/tags")
async def create_tag(
    tag_data: dict,
    db: Session = Depends(get_db)
):
    """创建新模型标签"""
    # 验证必填字段
    if "name" not in tag_data:
        raise HTTPException(status_code=400, detail="标签名称是必填字段")
    
    # 检查标签是否已存在
    existing = db.query(models.ModelTag).filter(
        models.ModelTag.name == tag_data["name"]
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="该标签已存在")
    
    tag = models.ModelTag(
        name=tag_data["name"],
        description=tag_data.get("description"),
        color=tag_data.get("color", "#3b82f6")
    )
    
    db.add(tag)
    db.commit()
    
    return {
        "id": tag.id,
        "name": tag.name,
        "message": "标签已创建"
    }


@app.put("/api/v1/tags/{tag_id}")
async def update_tag(
    tag_id: int,
    tag_data: dict,
    db: Session = Depends(get_db)
):
    """更新标签信息"""
    tag = db.query(models.ModelTag).filter(
        models.ModelTag.id == tag_id
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    
    if "name" in tag_data:
        # 检查新名称是否已存在
        existing = db.query(models.ModelTag).filter(
            models.ModelTag.name == tag_data["name"],
            models.ModelTag.id != tag_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="该标签名称已存在")
        tag.name = tag_data["name"]
    
    if "description" in tag_data:
        tag.description = tag_data["description"]
    
    if "color" in tag_data:
        tag.color = tag_data["color"]
    
    db.commit()
    
    return {"message": "标签已更新"}


@app.delete("/api/v1/tags/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    """删除标签"""
    tag = db.query(models.ModelTag).filter(
        models.ModelTag.id == tag_id
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    
    # 删除标签关联
    db.query(models.ModelTagRelation).filter(
        models.ModelTagRelation.tag_id == tag_id
    ).delete()
    
    db.delete(tag)
    db.commit()
    
    return {"message": "标签已删除"}


# ========== 模型标签关联API ==========

@app.get("/api/v1/models/{model_id}/tags")
async def get_model_tags(
    model_id: int,
    db: Session = Depends(get_db)
):
    """获取模型的所有标签"""
    model = db.query(models.AIModel).filter(
        models.AIModel.id == model_id
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="模型未找到")
    
    tags = db.query(models.ModelTag).join(
        models.ModelTagRelation,
        models.ModelTag.id == models.ModelTagRelation.tag_id
    ).filter(
        models.ModelTagRelation.model_id == model_id
    ).all()
    
    result = []
    for tag in tags:
        result.append({
            "id": tag.id,
            "name": tag.name,
            "color": tag.color,
            "description": tag.description
        })
    
    return {"tags": result}


@app.post("/api/v1/models/{model_id}/tags")
async def add_model_tags(
    model_id: int,
    tag_data: dict,
    db: Session = Depends(get_db)
):
    """为模型添加标签"""
    model = db.query(models.AIModel).filter(
        models.AIModel.id == model_id
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="模型未找到")
    
    tag_ids = tag_data.get("tag_ids", [])
    if not tag_ids:
        raise HTTPException(status_code=400, detail="标签ID列表不能为空")
    
    # 验证所有标签ID是否存在
    for tag_id in tag_ids:
        tag = db.query(models.ModelTag).filter(
            models.ModelTag.id == tag_id
        ).first()
        if not tag:
            raise HTTPException(status_code=400, detail=f"无效的标签ID: {tag_id}")
        
        # 检查是否已存在关联
        existing = db.query(models.ModelTagRelation).filter(
            models.ModelTagRelation.model_id == model_id,
            models.ModelTagRelation.tag_id == tag_id
        ).first()
        if not existing:
            relation = models.ModelTagRelation(
                model_id=model_id,
                tag_id=tag_id
            )
            db.add(relation)
    
    db.commit()
    
    return {"message": f"已为模型添加 {len(tag_ids)} 个标签"}


@app.delete("/api/v1/models/{model_id}/tags/{tag_id}")
async def remove_model_tag(
    model_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    """移除模型的标签"""
    relation = db.query(models.ModelTagRelation).filter(
        models.ModelTagRelation.model_id == model_id,
        models.ModelTagRelation.tag_id == tag_id
    ).first()
    
    if not relation:
        raise HTTPException(status_code=404, detail="标签关联未找到")
    
    db.delete(relation)
    db.commit()
    
    return {"message": "标签已移除"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # 修改为8001端口
