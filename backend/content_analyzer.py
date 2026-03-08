"""基于 Prompt 配置的内容分析器"""

import json
import re
from typing import Dict, Any, List, Optional
import openai
from anthropic import Anthropic


class ContentAnalyzer:
    """基于 Prompt 配置的内容分析器"""
    
    def __init__(self, config: Dict[str, str], prompt_config: Optional[Dict] = None):
        """
        初始化分析器
        
        Args:
            config: API 密钥配置
            prompt_config: Prompt 配置，包含分析维度等
        """
        self.config = config
        self.prompt_config = prompt_config or self._get_default_prompt_config()
        
        # 初始化 LLM 客户端
        self.openai_client = None
        self.anthropic_client = None
        self.deepseek_client = None
        
        if config.get("openai_api_key"):
            self.openai_client = openai.OpenAI(api_key=config["openai_api_key"])
        
        if config.get("claude_api_key"):
            self.anthropic_client = Anthropic(api_key=config["claude_api_key"])
        
        if config.get("deepseek_api_key"):
            self.deepseek_client = openai.OpenAI(
                api_key=config["deepseek_api_key"],
                base_url="https://api.deepseek.com"
            )
    
    def _get_default_prompt_config(self) -> Dict:
        """获取默认的 Prompt 配置"""
        return {
            "dimensions": [
                {
                    "name": "内容完整性",
                    "key": "content",
                    "weight": 0.30,
                    "description": "评估演讲内容是否覆盖了所有关键部分",
                    "criteria": [
                        "公司介绍：是否介绍了公司背景、业务范围",
                        "行业问题：是否说明了目标行业面临的痛点",
                        "技术方案：是否清晰描述了技术解决方案",
                        "核心优势：是否说明了与竞争对手的差异化优势",
                        "客户案例：是否提供了成功的客户案例",
                        "商业价值：是否说明了能带来的商业价值"
                    ]
                },
                {
                    "name": "逻辑结构",
                    "key": "logic",
                    "weight": 0.20,
                    "description": "评估演讲的逻辑结构是否清晰",
                    "criteria": [
                        "开场：是否有清晰的开场白和主题引入",
                        "问题引入：是否先说明问题再给出方案",
                        "递进逻辑：是否层层递进、环环相扣",
                        "总结：是否有清晰的总结和行动号召"
                    ]
                },
                {
                    "name": "客户理解度",
                    "key": "customer",
                    "weight": 0.20,
                    "description": "评估客户听完后的理解程度",
                    "criteria": [
                        "公司定位：客户能清楚知道公司是做什么的",
                        "问题认知：客户能理解所要解决的问题",
                        "价值认知：客户能理解产品/服务的价值",
                        "合作意愿：客户是否表现出继续了解的意愿"
                    ]
                },
                {
                    "name": "说服力",
                    "key": "persuasion",
                    "weight": 0.10,
                    "description": "评估演讲的说服力",
                    "criteria": [
                        "案例说服：是否有具体案例增强说服力",
                        "价值表达：是否清晰表达了商业价值",
                        "兴趣激发：是否成功激发客户兴趣"
                    ]
                }
            ],
            "system_prompt": "你是一位专业的销售演讲分析专家。请根据提供的演讲内容，客观、公正地评估各个维度的表现。",
            "output_format": "JSON"
        }
    
    def analyze_with_llm(self, transcript: str, dimension: Dict) -> Dict[str, Any]:
        """使用 LLM 分析单个维度"""
        prompt = self._build_analysis_prompt(transcript, dimension)
        
        # 优先使用 Claude，其次 OpenAI，最后 DeepSeek
        if self.anthropic_client:
            return self._call_claude(prompt, dimension)
        elif self.openai_client:
            return self._call_gpt(prompt, dimension)
        elif self.deepseek_client:
            return self._call_deepseek(prompt, dimension)
        else:
            # 没有配置 API Key 时，回退到简单的关键词匹配
            return self._fallback_keyword_analysis(transcript, dimension)
    
    def _build_analysis_prompt(self, transcript: str, dimension: Dict) -> str:
        """构建分析 Prompt"""
        criteria_text = "\n".join([f"- {c}" for c in dimension["criteria"]])
        
        prompt = f"""
{self.prompt_config.get("system_prompt", "")}

## 分析维度：{dimension["name"]}
**描述**：{dimension["description"]}
**评估标准**：
{criteria_text}

## 演讲内容：
```
{transcript}
```

## 任务：
请根据上述评估标准，对演讲内容进行分析，并按以下 JSON 格式返回结果：

```json
{{
    "score": 0-100,
    "analysis": "详细的分析说明，解释打分理由",
    "evidence": ["引用原文中的具体句子作为证据"],
    "suggestions": ["改进建议"]
}}
```

**要求**：
1. 评分要客观公正，不要过于宽松或严格
2. 分析说明要具体，指出优点和不足
3. evidence 必须引用原文中的具体句子
4. suggestions 要具体可执行
"""
        return prompt
    
    def _call_claude(self, prompt: str, dimension: Dict) -> Dict[str, Any]:
        """调用 Claude API"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.content[0].text
            return self._parse_llm_result(result_text, dimension)
        except Exception as e:
            return self._get_error_result(dimension, str(e))
    
    def _call_gpt(self, prompt: str, dimension: Dict) -> Dict[str, Any]:
        """调用 GPT API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            return self._parse_llm_result(result_text, dimension)
        except Exception as e:
            return self._get_error_result(dimension, str(e))
    
    def _call_deepseek(self, prompt: str, dimension: Dict) -> Dict[str, Any]:
        """调用 DeepSeek API"""
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            return self._parse_llm_result(result_text, dimension)
        except Exception as e:
            return self._get_error_result(dimension, str(e))
    
    def _parse_llm_result(self, result_text: str, dimension: Dict) -> Dict[str, Any]:
        """解析 LLM 返回结果"""
        try:
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(result_text)
            
            return {
                "key": dimension["key"],
                "name": dimension["name"],
                "score": result.get("score", 0),
                "analysis": result.get("analysis", ""),
                "evidence": result.get("evidence", []),
                "suggestions": result.get("suggestions", []),
                "criteria": dimension["criteria"]
            }
        except Exception as e:
            return self._get_error_result(dimension, str(e))
    
    def _fallback_keyword_analysis(self, transcript: str, dimension: Dict) -> Dict[str, Any]:
        """回退方案：简单的关键词分析（当没有配置 API Key 时）"""
        covered = 0
        for criteria in dimension["criteria"]:
            keyword = criteria.split(":")[0][:4] if ":" in criteria else criteria[:4]
            if keyword in transcript:
                covered += 1
        
        score = (covered / len(dimension["criteria"])) * 100 if dimension["criteria"] else 0
        
        return {
            "key": dimension["key"],
            "name": dimension["name"],
            "score": round(score, 2),
            "analysis": f"基于关键词匹配，覆盖了{covered}/{len(dimension['criteria'])}个评估标准",
            "evidence": [],
            "suggestions": ["建议配置 LLM API Key 以获得更准确的语义分析"],
            "criteria": dimension["criteria"]
        }
    
    def _get_error_result(self, dimension: Dict, error: str) -> Dict[str, Any]:
        """返回错误结果"""
        return {
            "key": dimension["key"],
            "name": dimension["name"],
            "score": 0,
            "analysis": f"分析失败：{error}",
            "evidence": [],
            "suggestions": ["请检查 API 配置"],
            "criteria": dimension["criteria"]
        }
    
    def analyze_all_dimensions(self, transcript: str) -> Dict[str, Any]:
        """分析所有维度"""
        results = {}
        total_score = 0
        total_weight = 0
        
        for dimension in self.prompt_config.get("dimensions", []):
            result = self.analyze_with_llm(transcript, dimension)
            results[dimension["key"]] = result
            
            weight = dimension.get("weight", 0)
            total_score += result["score"] * weight
            total_weight += weight
        
        return {
            "dimension_results": results,
            "total_score": round(total_score / total_weight, 2) if total_weight > 0 else 0,
            "weights": {d["key"]: d.get("weight", 0) for d in self.prompt_config.get("dimensions", [])}
        }
