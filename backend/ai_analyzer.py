from openai import OpenAI
from anthropic import Anthropic
from config import settings

class AIAnalyzer:
    def __init__(self):
        self.openai_client = None
        self.claude_client = None
        self.deepseek_client = None
        self.api_config = self._load_api_config()
    
    def _load_api_config(self):
        """加载API配置"""
        return {
            "openai": settings.OPENAI_API_KEY,
            "claude": settings.CLAUDE_API_KEY,
            "deepseek": settings.DEEPSEEK_API_KEY
        }
    
    def analyze_speech_expression(self, transcription):
        """分析表达能力"""
        prompt = f"""分析以下销售讲解的表达能力：

{transcription}

请分析：
1. 语速是否合适
2. 停顿是否合理
3. 流畅度如何
4. 是否有过多口头禅

请只根据提供的文本进行分析，不要脑补信息。如果无法判断，请说明。
"""
        
        try:
            if self.openai_client is None and self.api_config.get("openai"):
                self.openai_client = OpenAI(api_key=self.api_config.get("openai"))
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
        
        return "表达能力分析需要配置OpenAI API Key"
    
    def analyze_content_completeness(self, transcription):
        """分析内容完整度"""
        required_points = [
            "公司介绍",
            "行业问题",
            "技术方案",
            "核心优势",
            "客户案例",
            "商业价值"
        ]
        
        points_covered = []
        points_missing = []
        
        for point in required_points:
            if point in transcription:
                points_covered.append(point)
            else:
                points_missing.append(point)
        
        content_score = (len(points_covered) / len(required_points)) * 100
        
        return {
            "score": content_score,
            "covered": points_covered,
            "missing": points_missing
        }
    
    def analyze_logic_structure(self, transcription):
        """分析逻辑结构"""
        logic_points = [
            "是否有清晰开场",
            "是否有问题引入",
            "是否有递进逻辑",
            "是否有总结"
        ]
        
        logic_score = 0
        
        # 简单的逻辑检测（可以根据实际需求完善）
        if "大家好" in transcription or "早上好" in transcription or "下午好" in transcription:
            logic_score += 25
        
        if "问题" in transcription or "痛点" in transcription or "挑战" in transcription:
            logic_score += 25
        
        if "首先" in transcription and "然后" in transcription or "其次" in transcription or "最后" in transcription:
            logic_score += 25
        
        if "总结" in transcription or "综上所述" in transcription or "谢谢大家" in transcription:
            logic_score += 25
        
        return {
            "score": logic_score,
            "points": logic_points,
            "analysis": "逻辑结构分析完成"
        }
    
    def simulate_customer_understanding(self, transcription):
        """模拟客户理解度"""
        prompt = f"""现在请模拟一个普通客户，听完以下销售讲解后，回答以下问题：

销售讲解内容：
{transcription}

请回答：
1. 这家公司是做什么的？
2. 产品解决什么问题？
3. 为什么比别人好？
4. 是否愿意继续了解？

请只根据提供的文本进行回答，不要添加额外信息。如果无法回答，请明确说明。
"""
        
        try:
            if self.openai_client is None and self.api_config.get("openai"):
                self.openai_client = OpenAI(api_key=self.api_config.get("openai"))
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
        
        return "客户理解度模拟需要配置OpenAI API Key"
    
    def analyze_persuasion(self, transcription):
        """分析说服力"""
        persuasion_points = [
            "是否有客户案例",
            "是否有商业价值表达",
            "是否让人产生兴趣"
        ]
        
        persuasion_score = 0
        
        if "案例" in transcription or "客户" in transcription and "成功" in transcription:
            persuasion_score += 33
        
        if "价值" in transcription or "收益" in transcription or "效果" in transcription:
            persuasion_score += 33
        
        if "感兴趣" in transcription or "了解" in transcription or "咨询" in transcription:
            persuasion_score += 34
        
        return {
            "score": persuasion_score,
            "points": persuasion_points,
            "analysis": "说服力分析完成"
        }
    
    def generate_report(self, expression_analysis, content_analysis, logic_analysis, customer_analysis, persuasion_analysis):
        """生成综合分析报告"""
        total_score = self._calculate_total_score(
            expression_analysis,
            content_analysis,
            logic_analysis,
            customer_analysis,
            persuasion_analysis
        )
        
        report = {
            "total_score": total_score,
            "expression_score": expression_analysis.get("fluency_score", 0) * 0.2,
            "content_score": content_analysis.get("score", 0) * 0.3,
            "logic_score": logic_analysis.get("score", 0) * 0.2,
            "customer_score": self._calculate_customer_score(customer_analysis),
            "persuasion_score": persuasion_analysis.get("score", 0) * 0.1,
            "strengths": self._extract_strengths(
                expression_analysis,
                content_analysis,
                logic_analysis,
                customer_analysis,
                persuasion_analysis
            ),
            "weaknesses": self._extract_weaknesses(
                expression_analysis,
                content_analysis,
                logic_analysis,
                customer_analysis,
                persuasion_analysis
            ),
            "suggestions": self._generate_suggestions(
                expression_analysis,
                content_analysis,
                logic_analysis,
                customer_analysis,
                persuasion_analysis
            )
        }
        
        return report
    
    def _calculate_total_score(self, expression, content, logic, customer, persuasion):
        """计算总分"""
        expression_score = expression.get("fluency_score", 0) * 0.2
        content_score = content.get("score", 0) * 0.3
        logic_score = logic.get("score", 0) * 0.2
        customer_score = self._calculate_customer_score(customer)
        persuasion_score = persuasion.get("score", 0) * 0.1
        
        return round(expression_score + content_score + logic_score + customer_score + persuasion_score, 1)
    
    def _calculate_customer_score(self, customer_analysis):
        """计算客户理解度分数"""
        # 简单版本：检查是否能回答所有问题
        questions = ["做什么", "解决什么问题", "为什么比别人好", "愿意继续了解"]
        
        answered_count = 0
        for question in questions:
            if question in customer_analysis:
                answered_count += 1
        
        return (answered_count / len(questions)) * 20
    
    def _extract_strengths(self, expression, content, logic, customer, persuasion):
        """提取优点"""
        strengths = []
        
        if expression.get("fluency_score", 0) > 80:
            strengths.append("表达流畅，语速适中")
        
        if content.get("score", 0) > 80:
            strengths.append("内容覆盖全面")
        
        if logic.get("score", 0) > 80:
            strengths.append("逻辑结构清晰")
        
        if self._calculate_customer_score(customer) > 15:
            strengths.append("客户理解度高")
        
        if persuasion.get("score", 0) > 80:
            strengths.append("说服力强")
        
        return strengths
    
    def _extract_weaknesses(self, expression, content, logic, customer, persuasion):
        """提取问题"""
        weaknesses = []
        
        if expression.get("fluency_score", 0) < 60:
            weaknesses.append("表达不够流畅")
        
        if len(content.get("missing", [])) > 2:
            weaknesses.append(f"内容遗漏：{', '.join(content.get('missing', []))}")
        
        if logic.get("score", 0) < 60:
            weaknesses.append("逻辑结构不清晰")
        
        if self._calculate_customer_score(customer) < 10:
            weaknesses.append("客户理解度低")
        
        if expression.get("filler_words", 0) > 5:
            weaknesses.append("口头禅过多")
        
        return weaknesses
    
    def _generate_suggestions(self, expression, content, logic, customer, persuasion):
        """生成改进建议"""
        suggestions = []
        
        if expression.get("fluency_score", 0) < 80:
            suggestions.append("练习控制语速，减少不必要的停顿")
        
        if len(content.get("missing", [])) > 0:
            suggestions.append(f"补充以下内容：{', '.join(content.get('missing', []))}")
        
        if logic.get("score", 0) < 80:
            suggestions.append("优化讲解逻辑，确保有清晰的开场、递进和总结")
        
        if self._calculate_customer_score(customer) < 15:
            suggestions.append("提高讲解的通俗易懂性，确保客户能明白公司做什么、解决什么问题")
        
        if expression.get("filler_words", 0) > 5:
            suggestions.append("减少口头禅使用")
        
        return suggestions