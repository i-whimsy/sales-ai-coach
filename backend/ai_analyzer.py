"""AI analyzer module for AI Sales Coaching System"""

import openai
from anthropic import Anthropic
from typing import Dict, Any, List
import json


class AIAnalyzer:
    """Class for analyzing sales presentations using AI"""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize AI analyzer with API keys"""
        self.config = config
        self.openai_client = None
        self.anthropic_client = None
        self.deepseek_client = None
        
        # Initialize clients if API keys are provided
        if config.get("openai_api_key"):
            self.openai_client = openai.OpenAI(api_key=config["openai_api_key"])
        
        if config.get("claude_api_key"):
            self.anthropic_client = Anthropic(api_key=config["claude_api_key"])
    
    def analyze_content_completeness(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze content completeness based on predefined sections
        """
        sections = {
            "company_intro": "公司介绍",
            "industry_issues": "行业问题",
            "technical_solution": "技术方案",
            "core_advantages": "核心优势", 
            "customer_cases": "客户案例",
            "business_value": "商业价值"
        }
        
        scores = {}
        total_score = 0
        covered_sections = 0
        total_sections = len(sections)
        
        for section, chinese_keyword in sections.items():
            if chinese_keyword in transcript:
                scores[section] = 100
                covered_sections += 1
            else:
                scores[section] = 0
        
        if total_sections > 0:
            total_score = (covered_sections / total_sections) * 100
        
        return {
            "section_scores": scores,
            "total_score": round(total_score, 2),
            "covered_sections": covered_sections,
            "total_sections": total_sections
        }
    
    def analyze_logical_structure(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze logical structure of the presentation
        """
        structure_elements = {
            "clear_opening": "开场",
            "problem_introduction": "问题",
            "progressive_logic": "递进",
            "summary": "总结"
        }
        
        scores = {}
        total_score = 0
        covered_elements = 0
        total_elements = len(structure_elements)
        
        for element, chinese_keyword in structure_elements.items():
            if chinese_keyword in transcript:
                scores[element] = 100
                covered_elements += 1
            else:
                scores[element] = 0
        
        if total_elements > 0:
            total_score = (covered_elements / total_elements) * 100
        
        return {
            "structure_scores": scores,
            "total_score": round(total_score, 2),
            "covered_elements": covered_elements,
            "total_elements": total_elements
        }
    
    def analyze_customer_understanding(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze customer understanding by simulating customer comprehension
        """
        questions = [
            "这家公司是做什么的？",
            "产品解决什么问题？", 
            "为什么比别人好？",
            "是否愿意继续了解？"
        ]
        
        scores = {}
        total_score = 0
        answered_count = 0
        total_questions = len(questions)
        
        # For each question, check if transcript contains relevant information
        for question in questions:
            # Simple keyword matching approach
            if self._contains_relevant_info(transcript, question):
                scores[question] = 100
                answered_count += 1
            else:
                scores[question] = 0
        
        if total_questions > 0:
            total_score = (answered_count / total_questions) * 100
        
        return {
            "question_scores": scores,
            "total_score": round(total_score, 2),
            "answered_count": answered_count,
            "total_questions": total_questions
        }
    
    def _contains_relevant_info(self, transcript: str, question: str) -> bool:
        """
        Helper method to check if transcript contains relevant information for a question
        """
        if question == "这家公司是做什么的？":
            return "公司" in transcript or "产品" in transcript
        
        elif question == "产品解决什么问题？":
            return "问题" in transcript or "解决" in transcript
        
        elif question == "为什么比别人好？":
            return "优势" in transcript or "更好" in transcript
        
        elif question == "是否愿意继续了解？":
            return "感兴趣" in transcript or "了解" in transcript
        
        return False
    
    def analyze_persuasion(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze persuasion effectiveness
        """
        persuasion_elements = {
            "has_cases": "案例" in transcript,
            "has_value": "价值" in transcript,
            "generates_interest": "感兴趣" in transcript or "了解" in transcript
        }
        
        scores = {}
        total_score = 0
        positive_elements = 0
        total_elements = len(persuasion_elements)
        
        for element, has_element in persuasion_elements.items():
            scores[element] = 100 if has_element else 0
            if has_element:
                positive_elements += 1
        
        if total_elements > 0:
            total_score = (positive_elements / total_elements) * 100
        
        return {
            "element_scores": scores,
            "total_score": round(total_score, 2),
            "positive_elements": positive_elements,
            "total_elements": total_elements
        }
    
    def generate_report(self, transcript: str, speech_analysis: Dict, 
                      scoring_config: Dict = None) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report
        """
        if scoring_config is None:
            scoring_config = {
                "expression_weight": 0.20,
                "content_weight": 0.30,
                "logic_weight": 0.20,
                "customer_weight": 0.20,
                "persuasion_weight": 0.10
            }
        
        # Analyze different aspects
        content_analysis = self.analyze_content_completeness(transcript)
        logic_analysis = self.analyze_logical_structure(transcript)
        customer_analysis = self.analyze_customer_understanding(transcript)
        persuasion_analysis = self.analyze_persuasion(transcript)
        
        # Calculate weighted scores
        expression_score = speech_analysis["expression_score"]
        content_score = content_analysis["total_score"]
        logic_score = logic_analysis["total_score"]
        customer_score = customer_analysis["total_score"]
        persuasion_score = persuasion_analysis["total_score"]
        
        total_score = (
            (expression_score * scoring_config["expression_weight"]) +
            (content_score * scoring_config["content_weight"]) +
            (logic_score * scoring_config["logic_weight"]) +
            (customer_score * scoring_config["customer_weight"]) +
            (persuasion_score * scoring_config["persuasion_weight"])
        )
        
        # Generate report
        report = {
            "total_score": round(total_score, 2),
            "dimension_scores": {
                "expression": round(expression_score, 2),
                "content": round(content_score, 2),
                "logic": round(logic_score, 2),
                "customer_understanding": round(customer_score, 2),
                "persuasion": round(persuasion_score, 2)
            },
            "scores_weight": scoring_config,
            "speech_analysis": speech_analysis,
            "content_analysis": content_analysis,
            "logic_analysis": logic_analysis,
            "customer_analysis": customer_analysis,
            "persuasion_analysis": persuasion_analysis,
            "strengths": self._identify_strengths(transcript, speech_analysis, 
                                               content_analysis, logic_analysis,
                                               customer_analysis, persuasion_analysis),
            "improvement_suggestions": self._identify_improvements(transcript, 
                                                              speech_analysis, 
                                                              content_analysis, 
                                                              logic_analysis,
                                                              customer_analysis, 
                                                              persuasion_analysis)
        }
        
        return report
    
    def _identify_strengths(self, transcript: str, speech_analysis: Dict,
                          content_analysis: Dict, logic_analysis: Dict,
                          customer_analysis: Dict, persuasion_analysis: Dict) -> List[str]:
        """Identify strengths from analysis"""
        strengths = []
        
        if speech_analysis["expression_score"] > 80:
            strengths.append("表达能力强，语速适中，流畅度高")
        
        if content_analysis["total_score"] > 80:
            strengths.append("内容讲解全面，覆盖了所有重要部分")
        
        if logic_analysis["total_score"] > 80:
            strengths.append("逻辑结构清晰，有明确的开场、展开和总结")
        
        if customer_analysis["total_score"] > 80:
            strengths.append("讲解清晰，客户容易理解公司和产品价值")
        
        if persuasion_analysis["total_score"] > 80:
            strengths.append("说服力强，成功引起客户兴趣")
        
        if len(strengths) == 0:
            strengths.append("整体表现均衡，各个维度都有改进空间")
        
        return strengths
    
    def _identify_improvements(self, transcript: str, speech_analysis: Dict,
                             content_analysis: Dict, logic_analysis: Dict,
                             customer_analysis: Dict, persuasion_analysis: Dict) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        
        if speech_analysis["expression_score"] < 60:
            improvements.append("需要提高表达流畅度，减少口头禅和停顿")
        
        if content_analysis["total_score"] < 60:
            improvements.append("内容讲解不够全面，请确保覆盖公司介绍、行业问题、技术方案、核心优势、客户案例和商业价值")
        
        if logic_analysis["total_score"] < 60:
            improvements.append("逻辑结构需要优化，建议有更清晰的开场、问题引入、递进逻辑和总结")
        
        if customer_analysis["total_score"] < 60:
            improvements.append("讲解不够清晰，客户理解困难，建议简化语言，突出核心信息")
        
        if persuasion_analysis["total_score"] < 60:
            improvements.append("说服力不足，建议增加客户案例和价值表达，增强兴趣度")
        
        return improvements
