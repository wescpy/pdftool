#!/usr/bin/env python3
"""
Master test runner for the entire PDF Tool project.
Runs tests for backend, frontend, and CLI components.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, cwd=None, description=""):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running {description}...")
    print(f"Command: {' '.join(cmd)}")
    print(f"Working directory: {cwd or os.getcwd()}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, cwd=cwd, check=False, capture_output=False)
        success = result.returncode == 0
        print(f"\n✅ {description} {'PASSED' if success else 'FAILED'}")
        return success
    except Exception as e:
        print(f"\n❌ {description} ERROR: {e}")
        return False

def run_backend_tests():
    """Run backend tests."""
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Install test dependencies
    install_success = run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"],
        cwd=backend_dir,
        description="Installing backend test dependencies"
    )
    
    if not install_success:
        return False
    
    # Run tests
    return run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=backend_dir,
        description="Backend tests"
    )

def run_frontend_tests():
    """Run frontend tests."""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    install_success = run_command(
        ["npm", "install"],
        cwd=frontend_dir,
        description="Installing frontend dependencies"
    )
    
    if not install_success:
        return False
    
    # Run tests
    return run_command(
        ["npm", "run", "test:run"],
        cwd=frontend_dir,
        description="Frontend tests"
    )

def run_cli_tests():
    """Run CLI tests."""
    cli_dir = Path("cli")
    if not cli_dir.exists():
        print("❌ CLI directory not found")
        return False
    
    # Install test dependencies
    install_success = run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"],
        cwd=cli_dir,
        description="Installing CLI test dependencies"
    )
    
    if not install_success:
        return False
    
    # Run tests
    return run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=cli_dir,
        description="CLI tests"
    )

def main():
    """Run all test suites."""
    print("🚀 PDF Tool - Master Test Runner")
    print("Running all test suites...")
    
    results = {
        "backend": run_backend_tests(),
        "frontend": run_frontend_tests(),
        "cli": run_cli_tests()
    }
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST RESULTS SUMMARY")
    print('='*60)
    
    all_passed = True
    for component, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{component.upper():<10}: {status}")
        if not success:
            all_passed = False
    
    print('='*60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("The PDF Tool is ready for deployment.")
    else:
        print("⚠️  SOME TESTS FAILED!")
        print("Please fix the failing tests before deployment.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 