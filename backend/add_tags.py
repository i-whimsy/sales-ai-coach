
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import SessionLocal
import models

db = SessionLocal()

# Get models
whisper_model = db.query(models.AIModel).filter(models.AIModel.name == 'OpenAI Whisper API').first()
gpt_model = db.query(models.AIModel).filter(models.AIModel.name == 'OpenAI GPT-4o').first()

# Get tags
speech_tag = db.query(models.ModelTag).filter(models.ModelTag.name == '语音识别').first()
nlp_tag = db.query(models.ModelTag).filter(models.ModelTag.name == '自然语言处理').first()
chinese_tag = db.query(models.ModelTag).filter(models.ModelTag.name == '中文').first()

# Add tags to whisper model
if whisper_model and speech_tag:
    relation = models.ModelTagRelation(model_id=whisper_model.id, tag_id=speech_tag.id)
    db.add(relation)
    print(f'Added "{speech_tag.name}" tag to "{whisper_model.name}"')

# Add tags to GPT model
if gpt_model and nlp_tag:
    relation = models.ModelTagRelation(model_id=gpt_model.id, tag_id=nlp_tag.id)
    db.add(relation)
    print(f'Added "{nlp_tag.name}" tag to "{gpt_model.name}"')

if gpt_model and chinese_tag:
    relation = models.ModelTagRelation(model_id=gpt_model.id, tag_id=chinese_tag.id)
    db.add(relation)
    print(f'Added "{chinese_tag.name}" tag to "{gpt_model.name}"')

db.commit()
db.close()
