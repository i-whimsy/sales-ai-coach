#!/usr/bin/env python3
"""
Test script for Sales Audio Analyzer CLI
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

def test_audio_loader():
    """Test audio loader module"""
    print("Testing AudioLoader...")
    
    from modules.audio_loader import AudioLoader
    
    # Create test audio (sine wave)
    import numpy as np
    import soundfile as sf
    
    sample_rate = 16000
    duration = 2.0  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Save test file
    test_file = Path("test_audio.wav")
    sf.write(test_file, audio_data, sample_rate)
    
    # Test loader
    loader = AudioLoader(str(test_file))
    loader.load()
    
    info = loader.get_audio_info()
    print(f"  Duration: {info['duration_seconds']:.2f}s")
    print(f"  Sample rate: {info['sample_rate']} Hz")
    print(f"  [OK] AudioLoader test passed")
    
    # Cleanup
    test_file.unlink()
    
    return True


def test_vad_analyzer():
    """Test VAD analyzer"""
    print("\nTesting VADAnalyzer...")
    
    from modules.vad_analyzer import VADAnalyzer
    import numpy as np
    
    # Create test audio with silence
    sample_rate = 16000
    audio = np.concatenate([
        np.random.randn(sample_rate) * 0.1,  # 1s noise
        np.zeros(sample_rate),                # 1s silence
        np.random.randn(sample_rate) * 0.1,  # 1s noise
    ])
    
    vad = VADAnalyzer(threshold=0.5, sample_rate=sample_rate)
    result = vad.analyze(audio)
    
    print(f"  Speech ratio: {result['speech_ratio']:.1%}")
    print(f"  Pause count: {result['pause_count']}")
    print(f"  [OK] VADAnalyzer test passed")
    
    return True


def test_speech_to_text():
    """Test speech to text (requires actual audio)"""
    print("\nTesting SpeechToText...")
    print("  ⊘ Skipping (requires audio file)")
    return True


def test_prosody_analyzer():
    """Test prosody analyzer"""
    print("\nTesting ProsodyAnalyzer...")
    
    from modules.prosody_analyzer import ProsodyAnalyzer
    import numpy as np
    
    sample_rate = 16000
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    analyzer = ProsodyAnalyzer(sample_rate=sample_rate)
    result = analyzer.analyze(audio)
    
    print(f"  Pitch mean: {result.get('pitch_mean_hz', 0):.1f} Hz")
    print(f"  Energy mean: {result.get('energy_mean', 0):.4f}")
    print(f"  [OK] ProsodyAnalyzer test passed")
    
    return True


def test_filler_detector():
    """Test filler detector"""
    print("\nTesting FillerDetector...")
    
    from modules.filler_detector import FillerDetector
    
    # Test Chinese
    text_zh = "呃 然后 那个 我们公司的产品 其实 可能 大概 很好"
    detector_zh = FillerDetector(language='zh')
    result_zh = detector_zh.detect(text_zh)
    
    print(f"  Chinese text: {text_zh}")
    print(f"  Filler count: {result_zh['filler_word_count']}")
    print(f"  Fillers per 100w: {result_zh['fillers_per_100_words']:.1f}")
    
    # Test English
    text_en = "Um like you know basically I think it's good"
    detector_en = FillerDetector(language='en')
    result_en = detector_en.detect(text_en)
    
    print(f"  English text: {text_en}")
    print(f"  Filler count: {result_en['filler_word_count']}")
    print(f"  [OK] FillerDetector test passed")
    
    return True


def test_metrics_builder():
    """Test metrics builder"""
    print("\nTesting MetricsBuilder...")
    
    from modules.metrics_builder import MetricsBuilder
    
    builder = MetricsBuilder()
    
    # Mock data
    audio_info = {
        "file_path": "/test.wav",
        "file_name": "test.wav",
        "duration_seconds": 180,
        "sample_rate": 16000,
        "channels": 1,
        "file_size_bytes": 1024000,
        "file_size_mb": 1.0
    }
    
    vad_analysis = {
        "speech_duration": 150,
        "silence_duration": 30,
        "speech_ratio": 0.83,
        "pause_count": 15,
        "avg_pause_duration": 1.2,
        "long_pause_count": 3
    }
    
    transcript_result = {
        "text": "这是一个测试文本",
        "language": "zh",
        "model": "whisper-base",
        "words_total": 50
    }
    
    prosody_metrics = {
        "pitch_mean_hz": 150,
        "pitch_std_hz": 25,
        "pitch_range_hz": 100,
        "energy_mean": 0.25,
        "energy_std": 0.08,
        "energy_cv": 0.32
    }
    
    emotion_metrics = {
        "dominant_emotion": "neutral",
        "confidence": 0.75,
        "emotion_probabilities": {
            "neutral": 0.75,
            "happy": 0.15,
            "sad": 0.05,
            "angry": 0.03,
            "fear": 0.02
        }
    }
    
    filler_metrics = {
        "filler_word_count": 5,
        "filler_ratio": 0.1,
        "fillers_per_100_words": 10.0,
        "filler_by_type": {"然后": 3, "那个": 2}
    }
    
    metrics = builder.build(
        audio_info=audio_info,
        vad_analysis=vad_analysis,
        transcript_result=transcript_result,
        prosody_metrics=prosody_metrics,
        emotion_metrics=emotion_metrics,
        filler_metrics=filler_metrics
    )
    
    if builder.validate():
        print(f"  Metrics built successfully")
        print(f"  Total words: {metrics['speech_metrics']['words_total']}")
        print(f"  Speech ratio: {metrics['vad_analysis']['speech_ratio']:.1%}")
        print(f"  [OK] MetricsBuilder test passed")
        return True
    else:
        print(f"  ✗ MetricsBuilder validation failed")
        return False


def test_json_exporter():
    """Test JSON exporter"""
    print("\nTesting JSONExporter...")
    
    from modules.metrics_builder import MetricsBuilder
    from modules.json_exporter import JSONExporter
    
    builder = MetricsBuilder()
    
    # Build minimal metrics
    metrics = builder.build(
        audio_info={"file_name": "test.wav", "duration_seconds": 60, "sample_rate": 16000, "channels": 1, "file_size_bytes": 1000, "file_size_mb": 0.001, "file_path": "/test.wav"},
        vad_analysis={"speech_duration": 50, "silence_duration": 10, "speech_ratio": 0.83, "pause_count": 5, "avg_pause_duration": 1.0, "long_pause_count": 1},
        transcript_result={"text": "测试", "language": "zh", "model": "base", "words_total": 10},
        prosody_metrics={"pitch_mean_hz": 150, "pitch_std_hz": 20, "pitch_range_hz": 80, "energy_mean": 0.2, "energy_std": 0.05, "energy_cv": 0.25},
        emotion_metrics={"dominant_emotion": "neutral", "confidence": 0.7, "emotion_probabilities": {}},
        filler_metrics={"filler_word_count": 2, "filler_ratio": 0.2, "fillers_per_100_words": 20, "filler_by_type": {}}
    )
    
    exporter = JSONExporter()
    
    # Test export
    output_file = Path("test_output.json")
    path = exporter.export(metrics, str(output_file))
    
    print(f"  Exported to: {path}")
    
    # Verify file exists
    if output_file.exists():
        print(f"  [OK] JSONExporter test passed")
        output_file.unlink()  # Cleanup
        return True
    else:
        print(f"  ✗ JSONExporter test failed - file not created")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Sales Audio Analyzer CLI - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_audio_loader,
        test_vad_analyzer,
        test_speech_to_text,
        test_prosody_analyzer,
        test_filler_detector,
        test_metrics_builder,
        test_json_exporter
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [FAIL] Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Tests complete: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
