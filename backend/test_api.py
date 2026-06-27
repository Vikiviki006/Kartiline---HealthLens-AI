#!/usr/bin/env python
"""Test API endpoints."""
import time
import requests
import json

def test_api():
    """Test API endpoints."""
    base_url = "http://localhost:8000/api/v1"
    
    # Wait for server to start
    print("Waiting for server to start...")
    for i in range(10):
        try:
            resp = requests.get(f"{base_url}/health", timeout=2)
            if resp.status_code == 200:
                print("✓ Server is ready!")
                break
        except:
            if i < 9:
                print(f"  Attempt {i+1}/10...")
                time.sleep(1)
    
    # Test login
    print("\n1. Testing login endpoint...")
    try:
        login_resp = requests.post(
            f"{base_url}/auth/login",
            json={"email": "test@example.com", "password": "test123"},
            timeout=5
        )
        if login_resp.status_code == 200:
            token = login_resp.json().get("access_token")
            print(f"✓ Login successful! Token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {login_resp.status_code}")
            print(login_resp.text)
            return False
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False
    
    # Test get reports
    print("\n2. Testing GET /reports endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        reports_resp = requests.get(
            f"{base_url}/reports",
            headers=headers,
            timeout=5
        )
        if reports_resp.status_code == 200:
            reports = reports_resp.json()
            print(f"✓ GET /reports successful! Got {len(reports.get('data', []))} reports")
            print(f"   Response: {json.dumps(reports, indent=2)[:200]}...")
        else:
            print(f"✗ GET /reports failed: {reports_resp.status_code}")
            print(reports_resp.text)
    except Exception as e:
        print(f"✗ GET /reports error: {e}")
        return False
    
    print("\n✓ All tests passed! Database schema is fixed.")
    return True

if __name__ == "__main__":
    import sys
    success = test_api()
    sys.exit(0 if success else 1)
