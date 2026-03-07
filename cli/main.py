"""
SalesCoach CLI - Command Line Interface for Sales Presentation Analysis
"""
import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.core.speech_to_text import SpeechToText
from cli.core.speech_analysis import SpeechAnalyzer
from cli.core.content_analysis import ContentAnalyzer
from cli.core.scoring import ScoringEngine
from cli.config import DEFAULT_WEIGHTS

console = Console()


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
    
    Steps:
    1. Load audio
    2. Convert speech to text
    3. Analyze speech expression
    4. Analyze content
    5. Calculate scores
    6. Generate report
    """
    audio_path = Path(audio_file)
    audio_name = audio_path.stem
    
    console.print(f"\n[bold blue]SalesCoach Analysis[/bold blue]")
    console.print(f"File: {audio_file}")
    console.print(f"Model: {model}\n")
    
    # Set output directory
    if output:
        os.environ["SALESCOACH_OUTPUT"] = output
    
    # Step 1: Load audio info
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task1 = progress.add_task("Loading audio...", total=None)
        
        # Get audio duration (basic check)
        if not audio_path.exists():
            console.print(f"[red]Error: Audio file not found: {audio_file}[/red]")
            sys.exit(1)
        
        file_size = audio_path.stat().st_size / (1024 * 1024)  # MB
        console.print(f"  File size: {file_size:.2f} MB")
        progress.update(task1, completed=True)
    
    # Step 2: Speech to Text
    console.print("\n[yellow]Step 1/6:[/yellow] Speech to text")
    stt = SpeechToText(model_name=model)
    transcript_result = stt.transcribe(audio_file)
    transcript = transcript_result["text"]
    
    console.print(f"  Language: {transcript_result['language']}")
    console.print(f"  Duration: {transcript_result['duration']:.2f}s")
    console.print(f"  Text length: {len(transcript)} chars")
    
    # Save transcript
    stt.save_transcript(audio_file)
    console.print(f"  [green]Saved: outputs/{audio_name}/transcript.txt[/green]")
    
    # Step 3: Speech Analysis
    console.print("\n[yellow]Step 2/6:[/yellow] Speech analysis")
    speech_analyzer = SpeechAnalyzer()
    speech_result = speech_analyzer.analyze(transcript, audio_file)
    
    console.print(f"  Expression score: {speech_result['expression_score']}")
    console.print(f"  Speaking rate: {speech_result['metrics']['speaking_rate_wpm']} wpm")
    console.print(f"  Pause frequency: {speech_result['metrics']['pause_frequency_per_min']}/min")
    
    # Save speech analysis
    speech_analyzer.save_analysis(audio_file)
    console.print(f"  [green]Saved: outputs/{audio_name}/speech_analysis.json[/green]")
    
    # Step 4: Content Analysis
    console.print("\n[yellow]Step 3/6:[/yellow] Content analysis")
    content_analyzer = ContentAnalyzer(api_key=api_key)
    
    if use_ai and api_key:
        console.print("  Using AI-enhanced analysis...")
        content_result = content_analyzer.analyze_with_ai(transcript)
    else:
        content_result = content_analyzer.analyze(transcript)
    
    if "basic_analysis" in content_result:
        basic = content_result["basic_analysis"]
        console.print(f"  Content score: {basic['content_score']}")
        console.print(f"  Logic score: {basic['logic_score']}")
    else:
        console.print(f"  Content score: {content_result['content_score']}")
        console.print(f"  Logic score: {content_result['logic_score']}")
    
    # Save content analysis
    content_analyzer.save_analysis(audio_file, content_result)
    console.print(f"  [green]Saved: outputs/{audio_name}/content_analysis.json[/green]")
    
    # Step 5: Customer Simulation (simplified)
    console.print("\n[yellow]Step 4/6:[/yellow] Customer understanding analysis")
    # This is calculated in scoring
    
    # Step 6: Scoring
    console.print("\n[yellow]Step 5/6:[/yellow] Calculating scores")
    scorer = ScoringEngine(weights=DEFAULT_WEIGHTS)
    scores = scorer.calculate_score(speech_result, content_result)
    
    console.print(f"  Total score: {scores['total_score']}")
    
    # Step 7: Generate Report
    console.print("\n[yellow]Step 6/6:[/yellow] Generating report")
    report = scorer.generate_report(transcript, speech_result, content_result, scores)
    
    # Save report
    scorer.save_scores(audio_file, report)
    
    # Generate markdown report
    generate_markdown_report(audio_name, report, transcript)
    
    # Display results
    display_results(report)
    
    console.print(f"\n[green]Analysis complete![/green]")
    console.print(f"Output directory: outputs/{audio_name}/")


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option("--model", "-m", default="base", help="Whisper model size")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def transcript(audio_file: str, model: str, output: str):
    """
    Convert speech to text only.
    
    Outputs:
    - transcript.txt: Plain text transcript
    - transcript.json: Full metadata
    """
    console.print(f"\n[bold blue]Speech to Text[/bold blue]")
    console.print(f"File: {audio_file}")
    console.print(f"Model: {model}\n")
    
    stt = SpeechToText(model_name=model)
    output_path = stt.save_transcript(audio_file, output)
    
    console.print(f"[green]Transcript saved to: {output_path}[/green]")


@cli.command()
@click.argument("audio_file1", type=click.Path(exists=True))
@click.argument("audio_file2", type=click.Path(exists=True))
@click.option("--model", "-m", default="base", help="Whisper model size")
def compare(audio_file1: str, audio_file2: str, model: str):
    """
    Compare two presentation recordings.
    
    Shows differences in:
    - Content coverage
    - Structure
    - Scores
    """
    console.print(f"\n[bold blue]Comparing Presentations[/bold blue]\n")
    
    # Analyze both files
    files = [audio_file1, audio_file2]
    results = []
    
    for i, audio_file in enumerate(files, 1):
        console.print(f"Analyzing file {i}: {Path(audio_file).name}")
        
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
    console.print("\n[bold]Comparison Results:[/bold]\n")
    
    # Score comparison table
    table = Table(title="Score Comparison")
    table.add_column("Dimension", style="cyan")
    table.add_column(results[0]["name"], style="green")
    table.add_column(results[1]["name"], style="green")
    table.add_column("Difference", style="yellow")
    
    dims = ["expression", "content", "logic", "customer", "persuasion"]
    dim_names = ["Expression", "Content", "Logic", "Customer", "Persuasion"]
    
    for dim, name in zip(dims, dim_names):
        s1 = results[0]["scores"]["dimension_scores"][dim]
        s2 = results[1]["scores"]["dimension_scores"][dim]
        diff = s2 - s1
        diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
        table.add_row(name, f"{s1:.1f}", f"{s2:.1f}", diff_str)
    
    table.add_row("TOTAL", f"{results[0]['scores']['total_score']:.1f}", 
                  f"{results[1]['scores']['total_score']:.1f}", "")
    console.print(table)
    
    # Content comparison
    console.print("\n[bold]Content Coverage:[/bold]")
    for i, result in enumerate(results, 1):
        if "basic_analysis" in result["content"]:
            covered = result["content"]["basic_analysis"].get("content_covered", [])
        else:
            covered = result["content"].get("content_covered", [])
        console.print(f"\n{result['name']}:")
        console.print(f"  Covered: {', '.join(covered) if covered else 'None'}")
        
        if "basic_analysis" in result["content"]:
            missing = result["content"]["basic_analysis"].get("content_missing", [])
        else:
            missing = result["content"].get("content_missing", [])
        console.print(f"  Missing: {', '.join(missing) if missing else 'None'}")


def display_results(report: dict):
    """Display results in rich format"""
    console.print("\n" + "=" * 50)
    console.print("[bold]Sales Coaching Report[/bold]")
    console.print("=" * 50)
    
    # Score
    score = report["total_score"]
    score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    console.print(f"\n[bold]Total Score:[/bold] [{score_color}]{score}[/{score_color}]")
    
    # Dimension scores
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Dimension")
    table.add_column("Score")
    table.add_column("Weight")
    
    for dim, name in [("expression", "Expression"), ("content", "Content"),
                      ("logic", "Logic"), ("customer", "Customer"), 
                      ("persuasion", "Persuasion")]:
        score_val = report["dimension_scores"][dim]
        weight = int(DEFAULT_WEIGHTS[dim] * 100)
        table.add_row(name, f"{score_val}", f"{weight}%")
    
    console.print(table)
    
    # Strengths
    if report.get("strengths"):
        console.print("\n[bold green]Strengths:[/bold green]")
        for s in report["strengths"]:
            console.print(f"  ✓ {s}")
    
    # Issues
    if report.get("issues"):
        console.print("\n[bold red]Issues:[/bold red]")
        for i in report["issues"]:
            console.print(f"  ✗ {i}")
    
    # Suggestions
    if report.get("suggestions"):
        console.print("\n[bold yellow]Suggestions:[/bold yellow]")
        for s in report["suggestions"]:
            console.print(f"  → {s}")


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
    
    console.print(f"  [green]Saved: outputs/{audio_name}/report.md[/green]")


if __name__ == "__main__":
    cli()
