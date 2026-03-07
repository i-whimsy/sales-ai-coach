"""
Speech to Text module using Whisper
"""
import json
from pathlib import Path
from typing import Dict, Any

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


class SpeechToText:
    """Speech to text converter using Whisper"""
    
    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.model = None
        
    def load_model(self):
        """Load Whisper model"""
        if not WHISPER_AVAILABLE:
            raise ImportError("whisper not installed. Run: pip install openai-whisper")
        
        if self.model is None:
            print(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
        return self.model
    
    def transcribe(self, audio_path: str, language: str = "zh") -> Dict[str, Any]:
        """
        Transcribe audio to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (zh for Chinese, en for English)
            
        Returns:
            Dict with transcript, language, and metadata
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load model if not loaded
        self.load_model()
        
        # Transcribe
        result = self.model.transcribe(
            str(audio_path),
            language=language,
            verbose=False
        )
        
        return {
            "text": result["text"].strip(),
            "language": result["language"],
            "segments": len(result.get("segments", [])),
            "duration": result.get("duration", 0)
        }
    
    def save_transcript(self, audio_path: str, output_path: str = None) -> str:
        """
        Transcribe audio and save to file
        
        Args:
            audio_path: Path to audio file
            output_path: Optional output path. If None, saves to outputs/<name>/transcript.txt
            
        Returns:
            Path to saved transcript file
        """
        result = self.transcribe(audio_path)
        transcript_text = result["text"]
        
        if output_path is None:
            from config import get_output_dir
            output_dir = get_output_dir(audio_path)
            output_path = output_dir / "transcript.txt"
        
        # Save transcript
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        # Also save JSON metadata
        json_path = Path(output_path).with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return str(output_path)


def transcribe_audio(audio_path: str, output_path: str = None, model: str = "base") -> str:
    """
    Convenience function to transcribe audio
    
    Args:
        audio_path: Path to audio file
        output_path: Optional output path
        model: Whisper model size
        
    Returns:
        Path to saved transcript
    """
    stt = SpeechToText(model_name=model)
    return stt.save_transcript(audio_path, output_path)
