from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, create_database
from models import Recording
from speech_analysis import SpeechAnalyzer
from ai_analyzer import AIAnalyzer
from config import settings
import os
import tempfile
from datetime import datetime
import json

app = FastAPI(title="AI Sales Coaching System", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
create_database()

# 初始化分析器
speech_analyzer = SpeechAnalyzer()
ai_analyzer = AIAnalyzer()

@app.post("/api/upload")
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """音频上传"""
    try:
        # 保存文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        # 分析音频
        speech_analysis = speech_analyzer.analyze_speech(temp_file_path)
        
        # AI分析
        content_analysis = ai_analyzer.analyze_content_completeness(speech_analysis["transcription"])
        logic_analysis = ai_analyzer.analyze_logic_structure(speech_analysis["transcription"])
        customer_analysis = ai_analyzer.simulate_customer_understanding(speech_analysis["transcription"])
        persuasion_analysis = ai_analyzer.analyze_persuasion(speech_analysis["transcription"])
        
        # 生成报告
        report = ai_analyzer.generate_report(
            speech_analysis,
            content_analysis,
            logic_analysis,
            customer_analysis,
            persuasion_analysis
        )
        
        # 保存到数据库
        recording = Recording(
            file_name=file.filename,
            upload_time=datetime.utcnow(),
            score=report["total_score"],
            report_json=json.dumps(report, ensure_ascii=False)
        )
        
        db.add(recording)
        db.commit()
        db.refresh(recording)
        
        # 删除临时文件
        os.unlink(temp_file_path)
        
        return JSONResponse(content={
            "message": "Analysis completed successfully",
            "recording_id": recording.id,
            "report": report
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recordings")
async def get_recordings(db: Session = Depends(get_db)):
    """获取历史记录"""
    recordings = db.query(Recording).order_by(Recording.upload_time.desc()).all()
    
    return JSONResponse(content={
        "recordings": [{
            "id": recording.id,
            "file_name": recording.file_name,
            "upload_time": recording.upload_time.isoformat(),
            "score": recording.score
        } for recording in recordings]
    })

@app.get("/api/report/{recording_id}")
async def get_report(recording_id: int, db: Session = Depends(get_db)):
    """获取报告"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    try:
        report = json.loads(recording.report_json)
    except:
        report = {}
    
    return JSONResponse(content={
        "recording_id": recording.id,
        "file_name": recording.file_name,
        "report": report,
        "score": recording.score
    })

@app.get("/api/config")
async def get_config():
    """获取配置"""
    return JSONResponse(content={
        "api_keys": {
            "openai": len(settings.OPENAI_API_KEY) > 0,
            "claude": len(settings.CLAUDE_API_KEY) > 0,
            "deepseek": len(settings.DEEPSEEK_API_KEY) > 0,
            "whisper": len(settings.WHISPER_API_KEY) > 0
        }
    })

@app.post("/api/config")
async def set_config(openai_key: str = None, claude_key: str = None, deepseek_key: str = None, whisper_key: str = None):
    """保存配置"""
    if openai_key:
        settings.OPENAI_API_KEY = openai_key
    
    if claude_key:
        settings.CLAUDE_API_KEY = claude_key
    
    if deepseek_key:
        settings.DEEPSEEK_API_KEY = deepseek_key
    
    if whisper_key:
        settings.WHISPER_API_KEY = whisper_key
    
    return JSONResponse(content={"message": "Config updated successfully"})

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """根路径"""
    return {"message": "AI Sales Coaching System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)