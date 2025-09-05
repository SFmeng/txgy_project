#!/usr/bin/env python
import requests
import json

def test_login():
    url = 'http://localhost:8000/api/v1/auth/login/'
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()
        else:
            print("❌ Login failed!")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    test_login()
