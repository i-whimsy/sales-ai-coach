"""
Scoring module - generates final scores
"""
import json
from pathlib import Path
from typing import Dict, Any, List

from config import DEFAULT_WEIGHTS


class ScoringEngine:
    """Generate final scores based on analysis"""
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or DEFAULT_WEIGHTS
    
    def calculate_score(self, speech_analysis: Dict, content_analysis: Dict) -> Dict[str, Any]:
        """
        Calculate final scores
        
        Args:
            speech_analysis: Result from speech analysis
            content_analysis: Result from content analysis
            
        Returns:
            Dict with all scores
        """
        # Extract scores
        expression_score = speech_analysis.get("expression_score", 0)
        
        # Content analysis might have nested structure
        if "basic_analysis" in content_analysis:
            content_score = content_analysis["basic_analysis"].get("content_score", 0)
            logic_score = content_analysis["basic_analysis"].get("logic_score", 50)
        else:
            content_score = content_analysis.get("content_score", 0)
            logic_score = content_analysis.get("logic_score", 50)
        
        # Customer understanding score (simplified - based on content score)
        customer_score = min(100, content_score * 0.8 + 20)
        
        # Persuasion score (based on structure and logic)
        if "basic_analysis" in content_analysis:
            structure_score = content_analysis["basic_analysis"].get("structure_score", 50)
        else:
            structure_score = content_analysis.get("structure_score", 50)
        
        persuasion_score = (logic_score * 0.5 + structure_score * 0.5)
        
        # Calculate weighted total
        total_score = (
            expression_score * self.weights["expression"] +
            content_score * self.weights["content"] +
            logic_score * self.weights["logic"] +
            customer_score * self.weights["customer"] +
            persuasion_score * self.weights["persuasion"]
        )
        
        return {
            "total_score": round(total_score, 2),
            "dimension_scores": {
                "expression": round(expression_score, 2),
                "content": round(content_score, 2),
                "logic": round(logic_score, 2),
                "customer": round(customer_score, 2),
                "persuasion": round(persuasion_score, 2)
            },
            "weights_used": self.weights,
            "calculation": {
                "expression_contribution": round(expression_score * self.weights["expression"], 2),
                "content_contribution": round(content_score * self.weights["content"], 2),
                "logic_contribution": round(logic_score * self.weights["logic"], 2),
                "customer_contribution": round(customer_score * self.weights["customer"], 2),
                "persuasion_contribution": round(persuasion_score * self.weights["persuasion"], 2)
            }
        }
    
    def generate_report(self, transcript: str, speech_analysis: Dict, 
                       content_analysis: Dict, scores: Dict) -> Dict[str, Any]:
        """
        Generate full report
        
        Args:
            transcript: Full transcript
            speech_analysis: Speech analysis result
            content_analysis: Content analysis result
            scores: Calculated scores
            
        Returns:
            Complete report dict
        """
        # Determine strengths and issues
        strengths = []
        issues = []
        
        # Based on dimension scores
        if scores["dimension_scores"]["expression"] >= 80:
            strengths.append("表达流畅，语速适中")
        elif scores["dimension_scores"]["expression"] < 50:
            issues.append("表达不够流畅，建议改善语速和停顿")
        
        if scores["dimension_scores"]["content"] >= 80:
            strengths.append("内容完整，涵盖要点")
        elif scores["dimension_scores"]["content"] < 50:
            issues.append("内容不够完整，建议补充关键信息")
        
        if scores["dimension_scores"]["logic"] >= 80:
            strengths.append("逻辑清晰，结构合理")
        elif scores["dimension_scores"]["logic"] < 50:
            issues.append("逻辑结构需要改进")
        
        if scores["dimension_scores"]["customer"] >= 80:
            strengths.append("很好地理解客户需求")
        
        if scores["dimension_scores"]["persuasion"] >= 80:
            strengths.append("说服力强")
        elif scores["dimension_scores"]["persuasion"] < 50:
            issues.append("说服力不足，建议增加案例和数据")
        
        # Generate suggestions
        suggestions = []
        if scores["dimension_scores"]["content"] < 70:
            suggestions.append("增加产品/服务介绍的具体细节")
        if scores["dimension_scores"]["logic"] < 70:
            suggestions.append("优化演讲结构，使用清晰的过渡")
        if scores["dimension_scores"]["persuasion"] < 70:
            suggestions.append("增加真实客户案例和数据支撑")
        
        return {
            "total_score": scores["total_score"],
            "dimension_scores": scores["dimension_scores"],
            "transcript_preview": transcript[:500] + "..." if len(transcript) > 500 else transcript,
            "transcript_length": len(transcript),
            "strengths": strengths,
            "issues": issues,
            "suggestions": suggestions,
            "weights_used": self.weights
        }
    
    def save_scores(self, audio_path: str, result: Dict) -> str:
        """Save scores to file"""
        from config import get_output_dir
        
        output_dir = get_output_dir(audio_path)
        output_path = output_dir / "report.json"
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return str(output_path)


def calculate_scores(speech_analysis: Dict, content_analysis: Dict, 
                   weights: Dict = None) -> Dict[str, Any]:
    """
    Convenience function to calculate scores
    
    Args:
        speech_analysis: Speech analysis result
        content_analysis: Content analysis result
        weights: Optional custom weights
        
    Returns:
        Scores dict
    """
    engine = ScoringEngine(weights=weights)
    return engine.calculate_score(speech_analysis, content_analysis)
