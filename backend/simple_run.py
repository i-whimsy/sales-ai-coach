"""Simple runner without Unicode"""

import uvicorn
import os
import sys

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

# Import app
from new_app import app

if __name__ == "__main__":
    print("Starting AI Sales Coaching Backend v2.0.0")
    print("Access addresses:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("===============================================")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )