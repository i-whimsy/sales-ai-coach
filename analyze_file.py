#!/usr/bin/env python
import sys
import os
sys.path.insert(0, '.')

audio_file = r"C:\Users\clawbot\Downloads\202501\丁浩\丁浩第一题 - 客流.m4a"
output_file = r"C:\Users\clawbot\Downloads\202501\丁浩\analysis_result.json"

# Find the actual file
import glob
m4a_files = glob.glob(r"C:\Users\clawbot\Downloads\202501\丁浩\*.m4a")
print(f"Found {len(m4a_files)} m4a files:")
for f in m4a_files:
    print(f"  - {os.path.basename(f)}")

if m4a_files:
    audio_file = m4a_files[0]
    print(f"\nAnalyzing: {audio_file}")
    
    # Run analysis
    from modules.audio_loader import AudioLoader
    from modules.vad_analyzer import VADAnalyzer
    from modules.speech_to_text import SpeechToText
    from modules.prosody_analyzer import ProsodyAnalyzer
    from modules.filler_detector import FillerDetector
    from modules.metrics_builder import MetricsBuilder
    from modules.json_exporter import JSONExporter
    
    print("\n[STEP 1/7] Loading audio...")
    loader = AudioLoader(audio_file)
    loader.load()
    audio_info = loader.get_audio_info()
    print(f"  Duration: {audio_info['duration_seconds']:.2f}s")
    print(f"  Sample rate: {audio_info['sample_rate']} Hz")
    print("  [OK] Audio loaded")
    
    print("\n[STEP 2/7] VAD analysis...")
    vad = VADAnalyzer()
    vad_analysis = vad.analyze(loader.get_audio_data())
    print(f"  Speech ratio: {vad_analysis['speech_ratio']:.1%}")
    print("  [OK] VAD complete")
    
    print("\n[STEP 3/7] Speech to text...")
    stt = SpeechToText(model_name='base')
    transcript = stt.transcribe(audio_file)
    print(f"  Language: {transcript['language']}")
    print(f"  Word count: {transcript['words_total']}")
    print("  [OK] Transcription complete")
    
    print("\n[STEP 4/7] Prosody analysis...")
    prosody = ProsodyAnalyzer(sample_rate=audio_info['sample_rate'])
    prosody_metrics = prosody.analyze(loader.get_audio_data())
    speech_rate = prosody.calculate_speech_rate(transcript['text'], audio_info['duration_seconds'])
    prosody_metrics.update(speech_rate)
    print(f"  Pitch mean: {prosody_metrics['pitch_mean_hz']:.1f} Hz")
    print(f"  Speaking rate: {prosody_metrics['words_per_minute']:.1f} WPM")
    print("  [OK] Prosody complete")
    
    print("\n[STEP 5/7] Emotion... (skipped)")
    emotion_metrics = {"dominant_emotion": "neutral", "confidence": 0.5}
    
    print("\n[STEP 6/7] Filler detection...")
    filler = FillerDetector(language='zh')
    filler_metrics = filler.detect(transcript['text'])
    print(f"  Filler count: {filler_metrics['filler_word_count']}")
    print("  [OK] Filler detection complete")
    
    print("\n[STEP 7/7] Building metrics...")
    builder = MetricsBuilder()
    metrics = builder.build(
        audio_info=audio_info,
        vad_analysis=vad_analysis,
        transcript_result=transcript,
        prosody_metrics=prosody_metrics,
        emotion_metrics=emotion_metrics,
        filler_metrics=filler_metrics
    )
    print("  [OK] Metrics built")
    
    print("\n[OK] Exporting JSON...")
    exporter = JSONExporter()
    path = exporter.export(metrics, output_file)
    print(f"  [OK] JSON exported: {path}")
    
    print("\n" + "="*60)
    print("Analysis Summary")
    print("="*60)
    print(f"Duration: {audio_info['duration_seconds']:.1f}s | "
          f"Speed: {prosody_metrics['words_per_minute']:.1f} WPM | "
          f"Speech: {vad_analysis['speech_ratio']:.1%} | "
          f"Fillers: {filler_metrics['fillers_per_100_words']:.1f}/100w")
    print("\n[OK] Analysis complete!")
