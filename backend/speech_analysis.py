import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import os
import whisper
import tempfile

class SpeechAnalyzer:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        if self.model is None:
            try:
                self.model = whisper.load_model("base")
            except Exception as e:
                print(f"Error loading Whisper model: {e}")
                raise
    
    def analyze_speech(self, audio_file):
        """分析语音特征"""
        self.load_model()
        
        result = self.model.transcribe(audio_file)
        transcription = result.get("text", "")
        segments = result.get("segments", [])
        
        # 语速分析
        total_duration = sum(segment.get("end", 0) - segment.get("start", 0) for segment in segments)
        word_count = len(transcription.split())
        speech_rate = word_count / total_duration if total_duration > 0 else 0
        
        # 停顿检测
        pauses = []
        previous_end = 0
        
        for segment in segments:
            start = segment.get("start", 0)
            if previous_end > 0:
                pause = start - previous_end
                if pause > 0.5:  # 超过0.5秒的停顿
                    pauses.append(pause)
            previous_end = segment.get("end", 0)
        
        # 流畅度评分 (0-100)
        fluency_score = 100
        if len(segments) > 0:
            # 基于语速和停顿次数计算
            if speech_rate < 1 or speech_rate > 3:
                fluency_score -= 30
            if len(pauses) > len(segments) * 0.5:
                fluency_score -= 30
        
        # 口头禅检测 (简单版本)
       口头禅_count = 0
        口头禅_list = ["然后", "就是", "所以", "那个", "嗯", "啊", "呃"]
        for phrase in 口头禅_list:
            口头禅_count += transcription.lower().count(phrase)
        
        expression_analysis = {
            "speech_rate": speech_rate,
            "pauses": len(pauses),
            "fluency_score": fluency_score,
            "filler_words": 口头禅_count,
            "transcription": transcription
        }
        
        return expression_analysis
    
    def transcribe_audio(self, audio_file):
        """语音识别"""
        self.load_model()
        result = self.model.transcribe(audio_file)
        return result.get("text", "")