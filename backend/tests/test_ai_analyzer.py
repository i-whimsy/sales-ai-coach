import pytest
from ai_analyzer import AIAnalyzer

@pytest.fixture
def ai_analyzer():
    """创建带有测试配置的 AIAnalyzer 实例"""
    test_config = {
        "openai_api_key": "test_key",
        "claude_api_key": "test_key",
        "deepseek_api_key": "test_key",
        "whisper_api_key": "test_key"
    }
    return AIAnalyzer(test_config)

def test_ai_analyzer_initialization(ai_analyzer):
    """测试 AI 分析器初始化"""
    assert isinstance(ai_analyzer, AIAnalyzer)
    assert ai_analyzer.config is not None

def test_content_completeness_analysis(ai_analyzer):
    """测试内容完整度分析"""
    test_text = """
    大家好，我是某公司的销售。我们公司是做人工智能解决方案的，主要帮助企业解决数据分析问题。
    我们的技术方案采用了最新的机器学习技术，具有很强的技术优势。我们有很多成功的客户案例，
    比如帮助某知名企业提高了 30% 的效率，创造了显著的商业价值。
    """
    
    analysis = ai_analyzer.analyze_content_completeness(test_text)
    
    # 检查返回的键（实际 API 返回的键名）
    assert "total_score" in analysis or "score" in analysis
    assert "covered_sections" in analysis or "covered" in analysis
    assert "section_scores" in analysis
    assert isinstance(analysis.get("total_score", analysis.get("score")), (int, float))

def test_logic_analysis(ai_analyzer):
    """测试逻辑结构分析"""
    test_text = """
    大家好，我是某公司的销售。今天我来给大家介绍我们的产品。

    首先，我们来看看行业现状...

    然后，我们的产品解决方案...

    接下来，我来分享几个成功案例...

    最后，总结一下我们的优势...

    谢谢大家！
    """
    
    analysis = ai_analyzer.analyze_logical_structure(test_text)
    
    assert "total_score" in analysis or "score" in analysis
    assert "structure_scores" in analysis or "points" in analysis
    assert isinstance(analysis.get("total_score", analysis.get("score")), (int, float))

def test_persuasion_analysis(ai_analyzer):
    """测试说服力分析"""
    test_text = """
    我们的产品具有很强的优势，已经帮助很多客户取得了成功。
    比如某企业使用我们的产品后，效率提升了 30%，成本降低了 20%。
    我们的产品价值很高，能够帮助您的企业取得更好的业绩。
    """
    
    analysis = ai_analyzer.analyze_persuasion(test_text)
    
    assert "total_score" in analysis or "score" in analysis
    assert isinstance(analysis.get("total_score", analysis.get("score")), (int, float))
