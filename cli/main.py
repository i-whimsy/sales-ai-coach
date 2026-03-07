"""
SalesCoach CLI - Command Line Interface for Sales Presentation Analysis
"""
import os
import sys
from pathlib import Path

import click

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.core.speech_to_text import SpeechToText
from cli.core.speech_analysis import SpeechAnalyzer
from cli.core.content_analysis import ContentAnalyzer
from cli.core.scoring import ScoringEngine
from cli.config import DEFAULT_WEIGHTS


def print_step(step_num, total, description):
    """Print step progress"""
    print(f"\n[{step_num}/{total}] {description}")


def print_result(label, value):
    """Print result"""
    print(f"  {label}: {value}")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    SalesCoach - AI Sales Presentation Analyzer
    
    Analyze sales presentation recordings and generate coaching reports.
    """
    pass


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option("--model", "-m", default="base", help="Whisper model size (tiny, base, small, medium, large)")
@click.option("--api-key", "-k", envvar="OPENAI_API_KEY", help="OpenAI API key for AI analysis")
@click.option("--use-ai/--no-ai", default=False, help="Use AI for enhanced analysis")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
def analyze(audio_file: str, model: str, api_key: str, use_ai: bool, output: str):
    """
    Run full analysis pipeline on audio file.
    """
    audio_path = Path(audio_file)
    audio_name = audio_path.stem
    
    print(f"\n=== SalesCoach Analysis ===")
    print(f"File: {audio_file}")
    print(f"Model: {model}")
    
    # Set output directory
    if output:
        os.environ["SALESCOACH_OUTPUT"] = output
    
    # Step 1: Load audio info
    print_step(1, 6, "Loading audio...")
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)
    
    file_size = audio_path.stat().st_size / (1024 * 1024)
    print_result("File size", f"{file_size:.2f} MB")
    
    # Step 2: Speech to Text
    print_step(2, 6, "Speech to text")
    stt = SpeechToText(model_name=model)
    transcript_result = stt.transcribe(audio_file)
    transcript = transcript_result["text"]
    
    print_result("Language", transcript_result['language'])
    print_result("Duration", f"{transcript_result['duration']:.2f}s")
    print_result("Text length", f"{len(transcript)} chars")
    
    # Save transcript
    stt.save_transcript(audio_file)
    print_result("Saved", f"outputs/{audio_name}/transcript.txt")
    
    # Step 3: Speech Analysis
    print_step(3, 6, "Speech analysis")
    speech_analyzer = SpeechAnalyzer()
    speech_result = speech_analyzer.analyze(transcript, audio_file)
    
    print_result("Expression score", f"{speech_result['expression_score']}")
    print_result("Speaking rate", f"{speech_result['metrics']['speaking_rate_wpm']} wpm")
    print_result("Pause frequency", f"{speech_result['metrics']['pause_frequency_per_min']}/min")
    
    # Save speech analysis
    speech_analyzer.save_analysis(audio_file)
    print_result("Saved", f"outputs/{audio_name}/speech_analysis.json")
    
    # Step 4: Content Analysis
    print_step(4, 6, "Content analysis")
    content_analyzer = ContentAnalyzer(api_key=api_key)
    
    if use_ai and api_key:
        print("  Using AI-enhanced analysis...")
        content_result = content_analyzer.analyze_with_ai(transcript)
    else:
        content_result = content_analyzer.analyze(transcript)
    
    if "basic_analysis" in content_result:
        basic = content_result["basic_analysis"]
        print_result("Content score", f"{basic['content_score']}")
        print_result("Logic score", f"{basic['logic_score']}")
    else:
        print_result("Content score", f"{content_result['content_score']}")
        print_result("Logic score", f"{content_result['logic_score']}")
    
    # Save content analysis
    content_analyzer.save_analysis(audio_file, content_result)
    print_result("Saved", f"outputs/{audio_name}/content_analysis.json")
    
    # Step 5: Scoring
    print_step(5, 6, "Calculating scores")
    scorer = ScoringEngine(weights=DEFAULT_WEIGHTS)
    scores = scorer.calculate_score(speech_result, content_result)
    
    print_result("Total score", f"{scores['total_score']}")
    
    # Step 6: Generate Report
    print_step(6, 6, "Generating report")
    report = scorer.generate_report(transcript, speech_result, content_result, scores)
    
    # Save report
    scorer.save_scores(audio_file, report)
    
    # Generate markdown report
    generate_markdown_report(audio_name, report, transcript)
    
    # Display results
    display_results(report)
    
    print(f"\n=== Analysis Complete! ===")
    print(f"Output directory: outputs/{audio_name}/")


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option("--model", "-m", default="base", help="Whisper model size")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def transcript(audio_file: str, model: str, output: str):
    """
    Convert speech to text only.
    """
    print(f"\n=== Speech to Text ===")
    print(f"File: {audio_file}")
    print(f"Model: {model}")
    
    stt = SpeechToText(model_name=model)
    output_path = stt.save_transcript(audio_file, output)
    
    print(f"\nTranscript saved to: {output_path}")


@cli.command()
@click.argument("audio_file1", type=click.Path(exists=True))
@click.argument("audio_file2", type=click.Path(exists=True))
@click.option("--model", "-m", default="base", help="Whisper model size")
def compare(audio_file1: str, audio_file2: str, model: str):
    """
    Compare two presentation recordings.
    """
    print(f"\n=== Comparing Presentations ===\n")
    
    # Analyze both files
    files = [audio_file1, audio_file2]
    results = []
    
    for i, audio_file in enumerate(files, 1):
        print(f"Analyzing file {i}: {Path(audio_file).name}")
        
        stt = SpeechToText(model_name=model)
        transcript = stt.transcribe(audio_file)["text"]
        
        speech_analyzer = SpeechAnalyzer()
        speech_result = speech_analyzer.analyze(transcript, audio_file)
        
        content_analyzer = ContentAnalyzer()
        content_result = content_analyzer.analyze(transcript)
        
        scorer = ScoringEngine()
        scores = scorer.calculate_score(speech_result, content_result)
        
        results.append({
            "name": Path(audio_file).name,
            "transcript": transcript,
            "speech": speech_result,
            "content": content_result,
            "scores": scores
        })
    
    # Compare
    print("\n=== Comparison Results ===\n")
    
    # Score comparison
    print("Score Comparison:")
    print("-" * 50)
    print(f"{'Dimension':<20} {results[0]['name']:<15} {results[1]['name']:<15}")
    print("-" * 50)
    
    dims = ["expression", "content", "logic", "customer", "persuasion"]
    dim_names = ["Expression", "Content", "Logic", "Customer", "Persuasion"]
    
    for dim, name in zip(dims, dim_names):
        s1 = results[0]["scores"]["dimension_scores"][dim]
        s2 = results[1]["scores"]["dimension_scores"][dim]
        print(f"{name:<20} {s1:<15.1f} {s2:<15.1f}")
    
    print("-" * 50)
    print(f"{'TOTAL':<20} {results[0]['scores']['total_score']:<15.1f} {results[1]['scores']['total_score']:<15.1f}")
    
    # Content comparison
    print("\nContent Coverage:")
    for i, result in enumerate(results, 1):
        print(f"\n{result['name']}:")
        if "basic_analysis" in result["content"]:
            covered = result["content"]["basic_analysis"].get("content_covered", [])
            missing = result["content"]["basic_analysis"].get("content_missing", [])
        else:
            covered = result["content"].get("content_covered", [])
            missing = result["content"].get("content_missing", [])
        print(f"  Covered: {', '.join(covered) if covered else 'None'}")
        print(f"  Missing: {', '.join(missing) if missing else 'None'}")


def display_results(report: dict):
    """Display results"""
    print("\n" + "=" * 50)
    print("Sales Coaching Report")
    print("=" * 50)
    
    score = report["total_score"]
    print(f"\nTotal Score: {score}")
    
    print("\nDimension Scores:")
    print("-" * 30)
    for dim, name in [("expression", "Expression"), ("content", "Content"),
                      ("logic", "Logic"), ("customer", "Customer"), 
                      ("persuasion", "Persuasion")]:
        score_val = report["dimension_scores"][dim]
        weight = int(DEFAULT_WEIGHTS[dim] * 100)
        print(f"  {name:<15} {score_val:<10} ({weight}%)")
    
    # Strengths
    if report.get("strengths"):
        print("\nStrengths:")
        for s in report["strengths"]:
            print(f"  + {s}")
    
    # Issues
    if report.get("issues"):
        print("\nIssues:")
        for i in report["issues"]:
            print(f"  - {i}")
    
    # Suggestions
    if report.get("suggestions"):
        print("\nSuggestions:")
        for s in report["suggestions"]:
            print(f"  > {s}")


def generate_markdown_report(audio_name: str, report: dict, transcript: str):
    """Generate markdown report"""
    from config import get_output_dir
    
    output_dir = get_output_dir(audio_name)
    md_path = output_dir / "report.md"
    
    md_content = f"""# Sales Coaching Report

## Total Score: {report['total_score']}

## Dimension Scores

| Dimension | Score | Weight |
|-----------|-------|--------|
| Expression | {report['dimension_scores']['expression']} | 20% |
| Content | {report['dimension_scores']['content']} | 30% |
| Logic | {report['dimension_scores']['logic']} | 20% |
| Customer Understanding | {report['dimension_scores']['customer']} | 20% |
| Persuasion | {report['dimension_scores']['persuasion']} | 10% |

## Transcript

```
{transcript}
```

## Strengths

"""
    for s in report.get("strengths", []):
        md_content += f"- {s}\n"
    
    md_content += "\n## Issues\n\n"
    for i in report.get("issues", []):
        md_content += f"- {i}\n"
    
    md_content += "\n## Suggestions\n\n"
    for s in report.get("suggestions", []):
        md_content += f"- {s}\n"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"  Saved: outputs/{audio_name}/report.md")


if __name__ == "__main__":
    cli()
