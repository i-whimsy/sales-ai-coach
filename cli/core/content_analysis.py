"""
Content Analysis module - analyzes content completeness and quality
"""
import json
from pathlib import Path
from typing import Dict, Any, List

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config import CONTENT_CHECKLIST, STRUCTURE_CHECKLIST, CUSTOMER_QUESTIONS


class ContentAnalyzer:
    """Analyze content completeness and quality"""
    
    def __init__(self, api_key: str = None):
        self.client = None
        if api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=api_key)
    
    def analyze(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze content completeness
        
        Args:
            transcript: Transcribed text
            
        Returns:
            Dict with analysis results
        """
        # Check content checklist
        content_covered = []
        content_missing = []
        
        for item in CONTENT_CHECKLIST:
            if self._check_keyword_in_text(transcript, item):
                content_covered.append(item)
            else:
                content_missing.append(item)
        
        # Calculate content score
        content_score = (len(content_covered) / len(CONTENT_CHECKLIST)) * 100
        
        # Check structure
        structure_covered = []
        for item in STRUCTURE_CHECKLIST:
            if self._check_keyword_in_text(transcript, item):
                structure_covered.append(item)
        
        # Structure score
        structure_score = (len(structure_covered) / len(STRUCTURE_CHECKLIST)) * 100
        
        # Logic score (simplified - based on keywords)
        logic_keywords = ["首先", "其次", "然后", "最后", "第一", "第二", "第三",
                         "因为", "所以", "但是", "然而", "因此", "综上", "总之"]
        logic_count = sum(1 for kw in logic_keywords if kw in transcript)
        logic_score = min(100, 30 + logic_count * 10)
        
        return {
            "content_score": round(content_score, 2),
            "structure_score": round(structure_score, 2),
            "logic_score": round(logic_score, 2),
            "content_covered": content_covered,
            "content_missing": content_missing,
            "structure_covered": structure_covered,
            "assessment": self._generate_assessment(
                content_covered, content_missing, structure_covered, logic_score
            )
        }
    
    def analyze_with_ai(self, transcript: str) -> Dict[str, Any]:
        """
        Use AI to analyze content (requires OpenAI API)
        
        Args:
            transcript: Transcribed text
            
        Returns:
            Dict with AI analysis results
        """
        if not self.client:
            return self.analyze(transcript)
        
        prompt = f"""请分析以下销售演讲的内容质量：

演讲内容：
{transcript}

请从以下维度进行分析：
1. 内容完整性（是否涵盖：公司介绍、行业问题、技术方案、核心优势、客户案例、商业价值）
2. 逻辑结构（开场、问题引入、逻辑流、总结）
3. 说服力（案例、数据、价值表达）

请返回JSON格式的分析结果：
{{
    "content_score": 0-100,
    "structure_score": 0-100,
    "persuasion_score": 0-100,
    "strengths": ["优点1", "优点2"],
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Also run basic analysis
            basic = self.analyze(transcript)
            
            return {
                "ai_analysis": result,
                "basic_analysis": basic
            }
        except Exception as e:
            print(f"AI analysis failed: {e}, using basic analysis")
            return self.analyze(transcript)
    
    def _check_keyword_in_text(self, text: str, keyword: str) -> bool:
        """Check if keyword or related terms are in text"""
        # Direct match
        if keyword in text:
            return True
        
        # Related keywords mapping
        related = {
            "公司介绍": ["公司", "我们", "介绍", "创立", "成立于", "团队"],
            "行业问题": ["问题", "痛点", "挑战", "困难", "行业", "市场"],
            "技术方案": ["技术", "方案", "产品", "服务", "系统", "平台"],
            "核心优势": ["优势", "特点", "区别", "不同", "亮点", "竞争力"],
            "客户案例": ["案例", "客户", "合作", "成功", "实施", "落地"],
            "商业价值": ["价值", "收益", "回报", "成本", "节省", "提高"]
        }
        
        related_keywords = related.get(keyword, [])
        return any(kw in text for kw in related_keywords)
    
    def _generate_assessment(self, covered: List, missing: List, 
                           structure: List, logic_score: float) -> Dict[str, Any]:
        """Generate text assessment"""
        strengths = []
        issues = []
        
        if len(covered) >= 4:
            strengths.append("内容涵盖面较广")
        if len(structure) >= 3:
            strengths.append("结构清晰")
        if logic_score >= 60:
            strengths.append("逻辑性较强")
        
        if len(missing) >= 3:
            issues.append(f"缺少: {', '.join(missing[:3])}")
        if len(structure) < 2:
            issues.append("结构不够清晰")
        
        return {
            "strengths": strengths,
            "issues": issues
        }
    
    def save_analysis(self, audio_path: str, result: Dict) -> str:
        """Save analysis to file"""
        from config import get_output_dir
        
        output_dir = get_output_dir(audio_path)
        output_path = output_dir / "content_analysis.json"
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return str(output_path)


def analyze_content(transcript: str, use_ai: bool = False, api_key: str = None) -> Dict[str, Any]:
    """
    Convenience function to analyze content
    
    Args:
        transcript: Transcribed text
        use_ai: Whether to use AI for analysis
        api_key: OpenAI API key
        
    Returns:
        Analysis result dict
    """
    analyzer = ContentAnalyzer(api_key=api_key)
    if use_ai and api_key:
        return analyzer.analyze_with_ai(transcript)
    return analyzer.analyze(transcript)
