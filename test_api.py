#!/usr/bin/env python3
"""
Test the API directly
"""

import requests
import json

def test_chat():
    """Test the chat API"""
    
    url = "http://localhost:8001/chat"
    data = {
        "message": "what do i have to do to request a salary increase",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chat()
