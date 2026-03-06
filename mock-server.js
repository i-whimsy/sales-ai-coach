const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Mock data
const mockRecordings = [
  {
    id: 1,
    file_name: '销售录音1.mp3',
    upload_time: new Date().toISOString(),
    score: 85,
    status: 'analyzed'
  },
  {
    id: 2,
    file_name: '销售录音2.mp3',
    upload_time: new Date(Date.now() - 86400000).toISOString(),
    score: 78,
    status: 'analyzed'
  },
  {
    id: 3,
    file_name: '销售录音3.mp3',
    upload_time: new Date(Date.now() - 172800000).toISOString(),
    score: 92,
    status: 'analyzed'
  }
];

const mockReport = {
  total_score: 85,
  file_name: '销售录音1.mp3',
  transcript: '您好，我是大V公司的销售代表，很高兴为您介绍我们的产品。我们的产品具有很多优势，包括高品质、高性能、高可靠性等。',
  strengths: [
    '表达清晰流畅，语速适中',
    '内容覆盖全面，包含完整的产品介绍',
    '逻辑结构清晰，有明确的开场和总结',
    '使用了客户案例，增强了说服力'
  ],
  weaknesses: [
    '可以增加一些停顿，增强客户的理解和记忆',
    '产品优势的描述可以更加具体',
    '客户痛点的分析可以更加深入',
    '可以增加一些数据支持，增强可信度'
  ],
  suggestions: [
    '在介绍产品优势时，可以结合具体的数据和案例',
    '增加一些客户痛点的分析，让客户更有共鸣',
    '语速可以适当放慢，给客户更多思考时间',
    '增加一些互动环节，引导客户参与讨论'
  ],
  expression_score: 82,
  content_score: 90,
  logic_score: 85,
  customer_score: 78,
  persuasion_score: 88
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', version: '1.0.0' });
});

// Get all recordings
app.get('/api/v1/recordings', (req, res) => {
  res.json({ recordings: mockRecordings });
});

// Get recording by ID
app.get('/api/v1/recordings/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const recording = mockRecordings.find(r => r.id === id);
  if (!recording) {
    return res.status(404).json({ error: 'Recording not found' });
  }
  res.json({
    ...recording,
    transcript: mockReport.transcript,
    report: mockReport
  });
});

// Mock analysis endpoint
app.post('/api/v1/recordings/:id/analyze', (req, res) => {
  setTimeout(() => {
    const id = parseInt(req.params.id);
    const recording = mockRecordings.find(r => r.id === id);
    if (!recording) {
      return res.status(404).json({ error: 'Recording not found' });
    }
    res.json({
      id: recording.id,
      file_name: recording.file_name,
      total_score: mockReport.total_score,
      report: mockReport,
      status: 'analyzed'
    });
  }, 1000);
});

// Mock upload endpoint
app.post('/api/v1/recordings', (req, res) => {
  setTimeout(() => {
    const newRecording = {
      id: mockRecordings.length + 1,
      file_name: '上传的录音.mp3',
      upload_time: new Date().toISOString(),
      score: null,
      status: 'uploaded'
    };
    mockRecordings.push(newRecording);
    res.status(201).json({
      id: newRecording.id,
      file_name: newRecording.file_name,
      upload_time: newRecording.upload_time,
      status: newRecording.status
    });
  }, 1000);
});

// Delete recording
app.delete('/api/v1/recordings/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = mockRecordings.findIndex(r => r.id === id);
  if (index === -1) {
    return res.status(404).json({ error: 'Recording not found' });
  }
  mockRecordings.splice(index, 1);
  res.json({ message: 'Recording deleted successfully' });
});

// API config endpoints
app.get('/api/v1/api-config', (req, res) => {
  res.json({
    openai_api_key: null,
    deepseek_api_key: null,
    claude_api_key: null,
    whisper_api_key: null
  });
});

app.post('/api/v1/api-config', (req, res) => {
  res.json(req.body);
});

// Scoring config endpoints
app.get('/api/v1/scoring-config', (req, res) => {
  res.json({
    expression_weight: 0.20,
    content_weight: 0.30,
    logic_weight: 0.20,
    customer_weight: 0.20,
    persuasion_weight: 0.10
  });
});

app.post('/api/v1/scoring-config', (req, res) => {
  res.json(req.body);
});

// Serve static files if available
const frontendDistPath = path.join(__dirname, 'frontend', '.next');
if (require('fs').existsSync(frontendDistPath)) {
  app.use(express.static(path.join(__dirname, 'frontend')));
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
  });
}

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
  console.log(`🚀 Mock backend server running on http://localhost:${PORT}`);
  console.log('📊 AI Sales Coaching System - Mock Server');
  console.log('\nAvailable endpoints:');
  console.log('GET  /health - Health check');
  console.log('GET  /api/v1/recordings - List all recordings');
  console.log('GET  /api/v1/recordings/:id - Get recording details');
  console.log('POST /api/v1/recordings - Upload new recording');
  console.log('POST /api/v1/recordings/:id/analyze - Analyze recording');
  console.log('DELETE /api/v1/recordings/:id - Delete recording');
  console.log('GET  /api/v1/api-config - Get API configuration');
  console.log('POST /api/v1/api-config - Update API configuration');
  console.log('GET  /api/v1/scoring-config - Get scoring configuration');
  console.log('POST /api/v1/scoring-config - Update scoring configuration');
});
