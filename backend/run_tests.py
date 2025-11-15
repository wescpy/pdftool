#!/usr/bin/env python3
"""
Test runner script for the PDF Tool backend.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the backend test suite."""
    print("Running backend tests...")
    
    # Install test dependencies if needed
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing test dependencies: {e}")
        return False
    
    # Run tests
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], 
                              check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 