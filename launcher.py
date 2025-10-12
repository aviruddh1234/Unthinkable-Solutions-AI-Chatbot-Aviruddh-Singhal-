#!/usr/bin/env python3
"""
AI Customer Support Bot - Complete System Launcher
This script helps you start both backend and frontend components.
"""

import subprocess
import sys
import time
import requests
import threading
import os
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        ("flask", "flask"),
        ("gradio", "gradio"), 
        ("google-generativeai", "google.generativeai"),
        ("pandas", "pandas"),
        ("requests", "requests"),
        ("python-dotenv", "dotenv")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install requirements: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_env_file():
    """Check if .env file exists and has Gemini API key"""
    print("🔑 Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from template...")
        env_example = Path("env_example.txt")
        if env_example.exists():
            with open(env_example, 'r') as f:
                content = f.read()
            with open(".env", 'w') as f:
                f.write(content)
            print("📝 Created .env file. Please edit it with your Gemini API key.")
            return False
        else:
            print("❌ No env_example.txt file found")
            return False
    
    # Check if API key is set
    with open(".env", 'r') as f:
        content = f.read()
        if "your_gemini_api_key_here" in content:
            print("⚠️  Please set your Gemini API key in the .env file")
            return False
    
    print("✅ Environment configuration looks good")
    return True

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask Backend Server...")
    
    try:
        # Start backend in a separate process
        backend_process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for backend to start
        print("⏳ Waiting for backend to start...")
        time.sleep(3)
        
        # Check if backend is running
        try:
            response = requests.get("http://127.0.0.1:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully")
                return backend_process
            else:
                print("❌ Backend server failed to start properly")
                backend_process.terminate()
                return None
        except requests.exceptions.ConnectionError:
            print("❌ Backend server is not responding")
            backend_process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the Gradio frontend"""
    print("🎨 Starting Gradio Frontend...")
    
    try:
        # Start frontend
        frontend_process = subprocess.Popen([
            sys.executable, "chatbot_frontend.py"
        ])
        
        print("✅ Frontend server started successfully")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_frontend.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main launcher function"""
    print("🤖 AI Customer Support Bot - Complete System Launcher")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not Path("app.py").exists() or not Path("chatbot_frontend.py").exists():
        print("❌ Please run this script from the project root directory")
        print("Make sure both app.py and chatbot_frontend.py are present")
        return
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "start"
    
    if command == "test":
        print("🧪 Running in test mode...")
        if not check_requirements():
            return
        if not check_env_file():
            return
        
        # Start backend for testing
        backend_process = start_backend()
        if not backend_process:
            return
        
        try:
            if run_tests():
                print("✅ All tests passed!")
            else:
                print("❌ Some tests failed")
        finally:
            backend_process.terminate()
    
    elif command == "backend":
        print("🔧 Running backend only...")
        if not check_requirements():
            return
        if not check_env_file():
            return
        
        backend_process = start_backend()
        if backend_process:
            print("\n🛑 Press Ctrl+C to stop the backend")
            try:
                backend_process.wait()
            except KeyboardInterrupt:
                print("\n👋 Backend stopped by user")
                backend_process.terminate()
    
    elif command == "frontend":
        print("🎨 Running frontend only...")
        if not check_requirements():
            return
        
        print("⚠️  Make sure the backend is running at http://127.0.0.1:5000")
        frontend_process = start_frontend()
        if frontend_process:
            print("\n🛑 Press Ctrl+C to stop the frontend")
            try:
                frontend_process.wait()
            except KeyboardInterrupt:
                print("\n👋 Frontend stopped by user")
                frontend_process.terminate()
    
    elif command == "start":
        print("🚀 Running complete system...")
        if not check_requirements():
            return
        if not check_env_file():
            return
        
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            return
        
        # Start frontend
        frontend_process = start_frontend()
        if not frontend_process:
            backend_process.terminate()
            return
        
        print("\n" + "=" * 70)
        print("🎉 System is running!")
        print("📱 Frontend: http://localhost:7860")
        print("🔗 Backend API: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop both servers")
        print("=" * 70)
        
        try:
            # Wait for either process to finish
            while True:
                if backend_process.poll() is not None:
                    print("❌ Backend process stopped unexpectedly")
                    break
                if frontend_process.poll() is not None:
                    print("❌ Frontend process stopped unexpectedly")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Stopping both servers...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ Both servers stopped")
    
    else:
        print("Usage: python launcher.py [command]")
        print("\nCommands:")
        print("  start     - Start both backend and frontend (default)")
        print("  backend   - Start backend only")
        print("  frontend  - Start frontend only")
        print("  test      - Run tests")
        print("  help      - Show this help")
        print("\nGetting your Gemini API key:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Create API Key'")
        print("4. Copy the key and add it to your .env file")

if __name__ == "__main__":
    main()
