#!/usr/bin/env python3
"""
🌸 Cute Study Hub - Interactive Web Application Launcher ✨
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed."""
    try:
        import flask
        import flask_socketio
        import requests
        import bs4
        import PyPDF2
        import google.generativeai
        import openai
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        return False

def install_requirements():
    """Install requirements."""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_flask.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements!")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['uploads', 'templates', 'static']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("📁 Directories created successfully!")

def start_server():
    """Start the Flask server."""
    print("🚀 Starting Cute Study Hub Interactive Web Application...")
    print("=" * 60)
    print("🌸 Cute Study Hub - Interactive Web Application ✨")
    print("=" * 60)
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Features:")
    print("   🤖 AI Assistant with real-time responses")
    print("   🌐 Web Scraping with live updates")
    print("   📄 PDF Processing with drag & drop")
    print("   📝 Interactive Notes & Calendar")
    print("   👥 Study Groups management")
    print("   💬 Real-time AI Chat")
    print("   📊 Beautiful Dashboard")
    print("=" * 60)
    print("🎯 Open your browser and go to: http://localhost:5000")
    print("=" * 60)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the Flask app
    try:
        from app import app, socketio
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Cute Study Hub...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function."""
    print("🌸 Cute Study Hub - Interactive Web Application ✨")
    print("=" * 60)
    
    # Check if requirements are installed
    if not check_requirements():
        print("📦 Installing missing requirements...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("   pip install -r requirements_flask.txt")
            return
    
    # Create necessary directories
    create_directories()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
