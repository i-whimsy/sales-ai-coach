"""
Core modules for SalesCoach CLI
"""
from .speech_to_text import SpeechToText, transcribe_audio
from .speech_analysis import SpeechAnalyzer, analyze_speech
from .content_analysis import ContentAnalyzer, analyze_content
from .scoring import ScoringEngine, calculate_scores

__all__ = [
    "SpeechToText",
    "transcribe_audio",
    "SpeechAnalyzer",
    "analyze_speech",
    "ContentAnalyzer",
    "analyze_content",
    "ScoringEngine",
    "calculate_scores"
]
