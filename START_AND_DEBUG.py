#!/usr/bin/env python3
"""
Start server and capture errors
"""

import subprocess
import sys
import time
import requests

def start_server_and_debug():
    """Start server and debug errors"""
    print("STARTING SERVER WITH DEBUG")
    print("="*50)
    
    # Start server in background
    try:
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd="c:/Users/Javy/Desktop/skill swap", 
           stdout=subprocess.PIPE, 
           stderr=subprocess.PIPE,
           text=True)
        
        print("Server starting...")
        time.sleep(3)
        
        # Test endpoints
        test_results = {}
        
        # Test Admin
        try:
            response = requests.get("http://127.0.0.1:8000/admin/", timeout=5)
            test_results["Admin"] = response.status_code
        except Exception as e:
            test_results["Admin"] = f"Error: {e}"
        
        # Test Users API
        try:
            response = requests.get("http://127.0.0.1:8000/api/users/", timeout=5)
            test_results["Users API"] = response.status_code
        except Exception as e:
            test_results["Users API"] = f"Error: {e}"
        
        # Test Skills API
        try:
            response = requests.get("http://127.0.0.1:8000/api/skills/", timeout=5)
            test_results["Skills API"] = response.status_code
        except Exception as e:
            test_results["Skills API"] = f"Error: {e}"
        
        print("\nTEST RESULTS:")
        for endpoint, result in test_results.items():
            print(f"{endpoint}: {result}")
        
        # Get server output
        print("\nSERVER OUTPUT:")
        print("="*50)
        
        # Read stdout
        try:
            stdout, stderr = process.communicate(timeout=2)
            if stdout:
                print("STDOUT:")
                print(stdout)
            if stderr:
                print("STDERR:")
                print(stderr)
        except subprocess.TimeoutExpired:
            print("Server still running...")
            process.terminate()
        
        return test_results
        
    except Exception as e:
        print(f"Failed to start server: {e}")
        return {}

if __name__ == "__main__":
    start_server_and_debug()
