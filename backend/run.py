"""Simple runner for AI Sales Coaching Backend"""

import uvicorn
from new_app import app

if __name__ == "__main__":
    print("🚀 Starting AI Sales Coaching Backend v2.0.0")
    print("📋 Access addresses:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("===============================================")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )