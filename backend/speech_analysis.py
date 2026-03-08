"""Speech analysis module for AI Sales Coaching System"""

import numpy as np
import whisper
import librosa
import soundfile as sf
from typing import Tuple, Dict, Any, Optional
import re


class SpeechAnalyzer:
    """Class for analyzing speech characteristics from audio"""
    
    def __init__(self, model_name: str = "base", local_path: Optional[str] = None):
        """
        Initialize speech analyzer with configurable model
        
        Args:
            model_name: Whisper model name (tiny/base/small/medium/large)
            local_path: Optional custom model path or download root
        """
        self.model_name = model_name
        self.local_path = local_path
        
        # Load model with configured settings
        if local_path:
            self.whisper_model = whisper.load_model(model_name, download_root=local_path)
        else:
            self.whisper_model = whisper.load_model(model_name)
    
    def analyze_speech_rate(self, transcript: str, audio_duration: float) -> float:
        """
        Analyze speech rate (words per minute)
        """
        word_count = len(transcript.split())
        if audio_duration == 0:
            return 0.0
        
        words_per_minute = (word_count / audio_duration) * 60
        return round(words_per_minute, 2)
    
    def analyze_pauses(self, transcript: str) -> float:
        """
        Analyze pause patterns in speech
        """
        pause_patterns = re.findall(r'\.{3,}|[\n\r]{2,}', transcript)
        pause_count = len(pause_patterns)
        word_count = len(transcript.split())
        
        if word_count == 0:
            return 0.0
        
        pause_ratio = pause_count / word_count
        return round(pause_ratio * 100, 2)
    
    def analyze_fluency(self, transcript: str) -> float:
        """
        Analyze speech fluency
        """
        disfluencies = re.findall(r'um|uh|ah|like|you know|sort of|kind of', 
                                transcript.lower())
        word_count = len(transcript.split())
        
        if word_count == 0:
            return 0.0
        
        disfluency_ratio = len(disfluencies) / word_count
        fluency_score = max(0, 100 - (disfluency_ratio * 100))
        return round(fluency_score, 2)
    
    def analyze_mantras(self, transcript: str) -> float:
        """
        Analyze口头禅 (mantras) in speech
        """
        mantras = [
            '然后', '那个', '这个', '所以', '其实', '可能', '应该', 
            '大概', '就是', '等于', '比如', '或者', '但是', '而且'
        ]
        
        mantra_count = 0
        for mantra in mantras:
            mantra_count += transcript.count(mantra)
        
        word_count = len(transcript.split())
        
        if word_count == 0:
            return 0.0
        
        mantra_ratio = mantra_count / word_count
        mantra_score = max(0, 100 - (mantra_ratio * 100))
        return round(mantra_score, 2)
    
    def analyze_expression_quality(self, transcript: str, audio_duration: float) -> Dict[str, float]:
        """
        Analyze overall expression quality
        """
        speech_rate = self.analyze_speech_rate(transcript, audio_duration)
        pause_ratio = self.analyze_pauses(transcript)
        fluency_score = self.analyze_fluency(transcript)
        mantra_score = self.analyze_mantras(transcript)
        
        # Calculate expression score (weighted average)
        expression_score = (
            (speech_rate * 0.25) + 
            (pause_ratio * 0.25) + 
            (fluency_score * 0.25) + 
            (mantra_score * 0.25)
        )
        
        return {
            "speech_rate": speech_rate,
            "pause_ratio": pause_ratio,
            "fluency": fluency_score,
            "mantras": mantra_score,
            "expression_score": round(expression_score, 2)
        }
    
    def transcribe_audio(self, file_path: str) -> Tuple[str, float]:
        """
        Transcribe audio to text using Whisper
        """
        result = self.whisper_model.transcribe(file_path)
        transcript = result["text"]
        
        # Get audio duration
        audio, sr = librosa.load(file_path)
        duration = len(audio) / sr
        
        return transcript, duration
    
    def speech_to_text(self, file_path: str) -> str:
        """
        Convert speech to text
        """
        result = self.whisper_model.transcribe(file_path)
        return result["text"]
