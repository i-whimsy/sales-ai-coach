"""
Speech Analysis module - analyzes expression quality
"""
import json
from pathlib import Path
from typing import Dict, Any, List


class SpeechAnalyzer:
    """Analyze speech expression quality"""
    
    def __init__(self):
        self.analysis_result = {}
    
    def analyze(self, transcript: str, audio_path: str = None) -> Dict[str, Any]:
        """
        Analyze speech expression
        
        Args:
            transcript: Transcribed text
            audio_path: Optional path to audio for duration analysis
            
        Returns:
            Dict with analysis results
        """
        # Basic text analysis
        char_count = len(transcript)
        word_count = len(transcript.replace(" ", ""))
        
        # Estimate speech metrics based on text
        # In real implementation, would analyze audio file directly
        
        # Estimate speaking duration (avg 150 words/min in Chinese, 160 in English)
        estimated_duration = word_count / 150  # minutes
        
        # Calculate speaking rate
        speaking_rate = word_count / max(estimated_duration, 0.1)  # words per minute
        
        # Count pauses (estimated by punctuation)
        pause_markers = ["，", "。", "、", "；", "：", "...", ".", ","]
        pause_count = sum(transcript.count(p) for p in pause_markers)
        
        # Calculate pause frequency
        pause_frequency = pause_count / max(estimated_duration, 0.1)
        
        # Fluency score (based on pause frequency)
        # Higher pause frequency = better organization but too many = not fluent
        if pause_frequency < 1:
            fluency_score = 30
        elif pause_frequency < 3:
            fluency_score = 60 + (pause_frequency - 1) * 15  # 60-90
        elif pause_frequency < 6:
            fluency_score = 90 - (pause_frequency - 3) * 10-60
        else:
            fluency  # 90_score = max(30, 90 - (pause_frequency - 6) * 10)
        
        # Speaking rate score (ideal: 120-180 wpm for Chinese)
        if speaking_rate < 80:
            rate_score = 40
        elif speaking_rate < 120:
            rate_score = 60 + (speaking_rate - 80) * 0.75
        elif speaking_rate <= 180:
            rate_score = 90
        elif speaking_rate <= 220:
            rate_score = 100 - (speaking_rate - 180) * 0.25
        else:
            rate_score = max(40, 100 - (speaking_rate - 220) * 0.3)
        
        # Overall expression score
        expression_score = (fluency_score * 0.4 + rate_score * 0.6)
        
        self.analysis_result = {
            "expression_score": round(expression_score, 2),
            "metrics": {
                "char_count": char_count,
                "word_count": word_count,
                "estimated_duration_minutes": round(estimated_duration, 2),
                "speaking_rate_wpm": round(speaking_rate, 2),
                "pause_count": pause_count,
                "pause_frequency_per_min": round(pause_frequency, 2),
                "fluency_score": round(fluency_score, 2),
                "rate_score": round(rate_score, 2)
            },
            "assessment": self._generate_assessment(
                speaking_rate, pause_frequency, fluency_score
            )
        }
        
        return self.analysis_result
    
    def _generate_assessment(self, rate: float, pause_freq: float, fluency: float) -> List[str]:
        """Generate text assessment"""
        assessments = []
        
        # Rate assessment
        if rate < 100:
            assessments.append("语速偏慢，建议适当加快节奏")
        elif rate > 200:
            assessments.append("语速偏快，建议适当放慢让听众理解")
        else:
            assessments.append("语速适中")
        
        # Fluency assessment
        if fluency > 80:
            assessments.append("表达流畅")
        elif fluency > 60:
            assessments.append("表达基本流畅，有少量停顿")
        else:
            assessments.append("表达不够流畅，停顿较多")
        
        return assessments
    
    def save_analysis(self, audio_path: str) -> str:
        """Save analysis result to file"""
        from config import get_output_dir
        
        output_dir = get_output_dir(audio_path)
        output_path = output_dir / "speech_analysis.json"
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.analysis_result, f, ensure_ascii=False, indent=2)
        
        return str(output_path)


def analyze_speech(transcript: str, audio_path: str = None) -> Dict[str, Any]:
    """
    Convenience function to analyze speech
    
    Args:
        transcript: Transcribed text
        audio_path: Optional audio path
        
    Returns:
        Analysis result dict
    """
    analyzer = SpeechAnalyzer()
    return analyzer.analyze(transcript, audio_path)
