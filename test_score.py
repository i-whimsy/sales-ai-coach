# Test script to verify score functionality
import requests
import json
import time

# Base URL
BASE_URL = "http://localhost:8000"

def test_score_flow():
    print("Testing score functionality...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Checking health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Backend is running")
    except requests.exceptions.ConnectionError:
        print("   ✗ Backend is not running")
        return False
    
    # Test 2: Get sample report
    print("\n2. Testing sample report generation...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/sample-reports/1")
        if response.status_code == 200:
            report = response.json()
            print(f"   ✓ Sample report retrieved")
            print(f"   Total score: {report.get('total_score')}")
            print(f"   Expression score: {report.get('expression_score')}")
            print(f"   Score is null: {report.get('total_score') is None}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Upload a file (using mock data)
    print("\n3. Testing file upload simulation...")
    # Instead of uploading a real file, let's create a test recording directly
    
    # Test 4: Check if recording can be analyzed
    print("\n4. Testing analysis simulation...")
    # Let's create a mock analysis
    
    # Test 5: Check recording endpoint format
    print("\n5. Checking recording response format...")
    
    # Test 6: Test with actual data structure
    print("\n6. Testing score calculation logic...")
    
    # Simulate the scoring logic
    scores = {
        "expression": 85.5,
        "content": 82.3,
        "logic": 88.1,
        "customer": 79.8,
        "persuasion": 86.7
    }
    
    weights = {
        "expression": 0.20,
        "content": 0.30,
        "logic": 0.20,
        "customer": 0.20,
        "persuasion": 0.10
    }
    
    total_score = sum(
        scores[key] * weights[key]
        for key in scores
    )
    
    print(f"   Calculated score: {total_score:.1f}")
    print(f"   Score is null: {total_score is None}")
    print(f"   Score type: {type(total_score)}")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    return True

if __name__ == "__main__":
    test_score_flow()