#!/usr/bin/env python3
"""
Sales Audio Analyzer CLI
Command-line tool for objective audio feature extraction
"""

import sys
import json
from pathlib import Path
from datetime import datetime

import click
from tqdm import tqdm

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.audio_loader import AudioLoader
from modules.vad_analyzer import VADAnalyzer
from modules.speech_to_text import SpeechToText
from modules.prosody_analyzer import ProsodyAnalyzer
from modules.emotion_analyzer import EmotionAnalyzer
from modules.filler_detector import FillerDetector
from modules.metrics_builder import MetricsBuilder
from modules.json_exporter import JSONExporter


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Sales Audio Analyzer CLI
    
    Extract objective speech metrics from audio files.
    Output structured JSON for LLM analysis.
    """
    pass


@cli.command()
@click.argument('audio_file', type=click.Path(exists=True))
@click.option('--config', '-c', 'config_file', 
              type=click.Path(exists=True), 
              default='config.json',
              help='Configuration file')
@click.option('--output', '-o', 'output_file',
              type=click.Path(),
              default=None,
              help='Output JSON file path')
@click.option('--model', '-m', 'stt_model',
              default='base',
              help='Whisper model (tiny/base/small/medium/large)')
@click.option('--show-progress', '-p', is_flag=True,
              help='Show progress bars')
@click.option('--save-transcript', '-t', is_flag=True,
              help='Save transcript separately')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
@click.option('--no-emotion', is_flag=True,
              help='Skip emotion analysis')
@click.option('--export-llm-prompt', is_flag=True,
              help='Export LLM prompt template')
def analyze(
    audio_file: str,
    config_file: str,
    output_file: str,
    stt_model: str,
    show_progress: bool,
    save_transcript: bool,
    verbose: bool,
    no_emotion: bool,
    export_llm_prompt: bool
):
    """
    Analyze audio file and extract objective metrics.
    
    AUDIO_FILE: Path to audio file (wav, mp3, m4a, etc.)
    
    Example:
    
    \b
        python cli.py analyze demo.wav
        python cli.py analyze demo.wav -o result.json
        python cli.py analyze demo.wav --model large --show-progress
    """
    # Load configuration
    config = load_config(config_file)
    
    # Setup progress
    use_tqdm = show_progress or verbose
    
    click.echo("=" * 60)
    click.echo("Sales Audio Analyzer CLI")
    click.echo("=" * 60)
    click.echo(f"Input: {audio_file}")
    click.echo(f"Model: {stt_model}")
    click.echo("")
    
    try:
        # STEP 1: Load audio
        click.echo("[STEP 1/7] Loading audio...")
        audio_loader = AudioLoader(audio_file)
        audio_loader.load()
        audio_loader.validate(max_duration=config.get('features', {}).get('skip_if_too_long', 3600))
        audio_info = audio_loader.get_audio_info()
        
        if verbose:
            click.echo(f"  Duration: {audio_info['duration_seconds']:.2f}s")
            click.echo(f"  Sample rate: {audio_info['sample_rate']} Hz")
            click.echo(f"  File size: {audio_info['file_size_mb']:.2f} MB")
        click.echo("  [OK] Audio loaded")
        click.echo("")
        
        # STEP 2: VAD analysis
        click.echo("[STEP 2/7] Voice activity detection...")
        vad_analyzer = VADAnalyzer(
            threshold=config.get('models', {}).get('vad', {}).get('threshold', 0.5)
        )
        vad_analysis = vad_analyzer.analyze(audio_loader.get_audio_data())
        
        if verbose:
            click.echo(f"  Speech ratio: {vad_analysis['speech_ratio']:.1%}")
            click.echo(f"  Pause count: {vad_analysis['pause_count']}")
        click.echo("  [OK] VAD analysis complete")
        click.echo("")
        
        # STEP 3: Speech to text
        click.echo("[STEP 3/7] Speech to text...")
        stt = SpeechToText(model_name=stt_model)
        transcript_result = stt.transcribe(audio_file)
        
        if verbose:
            click.echo(f"  Language: {transcript_result['language']}")
            click.echo(f"  Word count: {transcript_result['words_total']}")
        
        if save_transcript:
            transcript_path = stt.save_transcript(audio_file)
            if verbose:
                click.echo(f"  Transcript saved: {transcript_path}")
        
        click.echo("  [OK] Transcription complete")
        click.echo("")
        
        # STEP 4: Prosody analysis
        click.echo("[STEP 4/7] Prosody analysis...")
        prosody_analyzer = ProsodyAnalyzer(sample_rate=audio_info['sample_rate'])
        prosody_metrics = prosody_analyzer.analyze(audio_loader.get_audio_data())
        
        # Add speech rate
        speech_rate = prosody_analyzer.calculate_speech_rate(
            transcript_result['text'],
            audio_info['duration_seconds']
        )
        prosody_metrics.update(speech_rate)
        
        if verbose:
            click.echo(f"  Pitch mean: {prosody_metrics['pitch_mean_hz']:.1f} Hz")
            click.echo(f"  Speaking rate: {prosody_metrics['words_per_minute']:.1f} WPM")
        click.echo("  [OK] Prosody analysis complete")
        click.echo("")
        
        # STEP 5: Emotion recognition
        if not no_emotion and config.get('features', {}).get('enable_emotion', True):
            click.echo("[STEP 5/7] Emotion recognition...")
            emotion_analyzer = EmotionAnalyzer()
            emotion_metrics = emotion_analyzer.analyze(audio_file)
            
            if verbose:
                click.echo(f"  Dominant emotion: {emotion_metrics['dominant_emotion']}")
                click.echo(f"  Confidence: {emotion_metrics['confidence']:.1%}")
            click.echo("  [OK] Emotion analysis complete")
        else:
            click.echo("[STEP 5/7] Emotion recognition... (skipped)")
            emotion_metrics = {
                "dominant_emotion": "neutral",
                "confidence": 0.5,
                "emotion_probabilities": {},
                "note": "Emotion analysis disabled"
            }
        click.echo("")
        
        # STEP 6: Filler word detection
        click.echo("[STEP 6/7] Filler word detection...")
        filler_detector = FillerDetector(language=transcript_result.get('language', 'zh'))
        filler_metrics = filler_detector.detect(transcript_result['text'])
        
        if verbose:
            click.echo(f"  Filler count: {filler_metrics['filler_word_count']}")
            click.echo(f"  Ratio: {filler_metrics['fillers_per_100_words']:.1f} per 100 words")
        click.echo("  [OK] Filler detection complete")
        click.echo("")
        
        # STEP 7: Build metrics
        click.echo("[STEP 7/7] Building metrics...")
        metrics_builder = MetricsBuilder()
        metrics = metrics_builder.build(
            audio_info=audio_info,
            vad_analysis=vad_analysis,
            transcript_result=transcript_result,
            prosody_metrics=prosody_metrics,
            emotion_metrics=emotion_metrics,
            filler_metrics=filler_metrics
        )
        
        # Validate
        if not metrics_builder.validate():
            click.echo("  [WARN] Warning: Metrics validation failed")
        click.echo("  [OK] Metrics built")
        click.echo("")
        
        # Export results
        if output_file is None:
            # Generate output path
            audio_path = Path(audio_file)
            output_dir = Path("outputs") / audio_path.stem
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "analysis_result.json"
        
        exporter = JSONExporter(
            indent=config.get('output', {}).get('indent', 2),
            ensure_ascii=config.get('output', {}).get('ensure_ascii', False)
        )
        
        # Export JSON
        json_path = exporter.export(
            metrics,
            output_file,
            include_transcript=config.get('output', {}).get('include_transcript', True)
        )
        click.echo(f"[OK] JSON exported: {json_path}")
        
        # Export LLM prompt if requested
        if export_llm_prompt:
            prompt_template = load_prompt_template()
            prompt_path = Path(output_file).parent / "llm_prompt.txt"
            
            exporter.generate_llm_prompt(
                metrics,
                prompt_template,
                str(prompt_path)
            )
            click.echo(f"[OK] LLM prompt exported: {prompt_path}")
        
        # Print summary
        click.echo("")
        click.echo("=" * 60)
        click.echo("Analysis Summary")
        click.echo("=" * 60)
        click.echo(exporter._create_summary_report(metrics))
        click.echo("")
        click.echo("[OK] Analysis complete!")
        click.echo("")
        
    except Exception as e:
        click.echo(f"[ERROR] Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('audio_file', type=click.Path(exists=True))
@click.option('--model', '-m', 'stt_model', default='base', help='Whisper model')
@click.option('--output', '-o', type=click.Path(), default=None, help='Output file')
def transcribe(audio_file: str, stt_model: str, output: str):
    """
    Transcribe audio to text only.
    
    AUDIO_FILE: Path to audio file
    """
    click.echo(f"Transcribing: {audio_file}")
    click.echo(f"Model: {stt_model}")
    click.echo("")
    
    stt = SpeechToText(model_name=stt_model)
    result = stt.transcribe(audio_file)
    
    if output:
        output_path = stt.save_transcript(audio_file, output)
        click.echo(f"Transcript saved: {output_path}")
    else:
        click.echo("Transcript:")
        click.echo("-" * 60)
        click.echo(result['text'])
        click.echo("-" * 60)


@cli.command()
@click.argument('audio_file1', type=click.Path(exists=True))
@click.argument('audio_file2', type=click.Path(exists=True))
@click.option('--model', '-m', default='base', help='Whisper model')
def compare(audio_file1: str, audio_file2: str, model: str):
    """
    Compare two audio files.
    
    AUDIO_FILE1: First audio file
    AUDIO_FILE2: Second audio file
    """
    click.echo("Comparing two audio files...")
    click.echo("")
    
    files = [audio_file1, audio_file2]
    results = []
    
    for audio_file in files:
        click.echo(f"Analyzing: {Path(audio_file).name}")
        
        # Quick analysis
        audio_loader = AudioLoader(audio_file)
        audio_loader.load()
        
        stt = SpeechToText(model_name=model)
        transcript = stt.transcribe(audio_file)
        
        prosody_analyzer = ProsodyAnalyzer(sample_rate=audio_loader.get_audio_info()['sample_rate'])
        prosody = prosody_analyzer.analyze(audio_loader.get_audio_data())
        speech_rate = prosody_analyzer.calculate_speech_rate(
            transcript['text'],
            audio_loader.get_audio_info()['duration_seconds']
        )
        
        filler_detector = FillerDetector()
        fillers = filler_detector.detect(transcript['text'])
        
        results.append({
            'file': Path(audio_file).name,
            'duration': audio_loader.get_audio_info()['duration_seconds'],
            'wpm': speech_rate['words_per_minute'],
            'fillers_per_100w': fillers['fillers_per_100_words'],
            'pitch_mean': prosody['pitch_mean_hz']
        })
        
        click.echo("  [OK] Done")
        click.echo("")
    
    # Compare
    click.echo("=" * 60)
    click.echo("Comparison Results")
    click.echo("=" * 60)
    click.echo(f"{'Metric':<25} {results[0]['file']:<15} {results[1]['file']:<15}")
    click.echo("-" * 60)
    click.echo(f"{'Duration (s)':<25} {results[0]['duration']:<15.1f} {results[1]['duration']:<15.1f}")
    click.echo(f"{'Speaking Rate (WPM)':<25} {results[0]['wpm']:<15.1f} {results[1]['wpm']:<15.1f}")
    click.echo(f"{'Fillers/100w':<25} {results[0]['fillers_per_100w']:<15.1f} {results[1]['fillers_per_100w']:<15.1f}")
    click.echo(f"{'Pitch Mean (Hz)':<25} {results[0]['pitch_mean']:<15.1f} {results[1]['pitch_mean']:<15.1f}")
    click.echo("=" * 60)


def load_config(config_file: str) -> dict:
    """Load configuration from file"""
    config_path = Path(config_file)
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Default config
    return {
        "models": {
            "speech_to_text": {"provider": "whisper", "model": "base"},
            "vad": {"provider": "silero", "threshold": 0.5},
            "emotion": {"provider": "speechbrain"}
        },
        "audio_analysis": {
            "enable_pitch": True,
            "enable_energy": True,
            "enable_pause": True
        },
        "output": {
            "indent": 2,
            "ensure_ascii": False,
            "include_transcript": True
        }
    }


def load_prompt_template() -> str:
    """Load LLM prompt template"""
    template_path = Path(__file__).parent / "prompt_template.txt"
    
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    # Default template
    return """You are a sales training expert.

Below is objective speech analysis data from a sales presentation.

Please analyze:
1. Expression quality
2. Clarity and understandability
3. Strengths
4. Areas for improvement
5. Specific recommendations

Analysis data:

{{analysis_json}}
"""


if __name__ == '__main__':
    cli()
