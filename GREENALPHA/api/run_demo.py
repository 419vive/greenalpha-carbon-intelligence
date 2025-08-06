#!/usr/bin/env python3
"""
GreenAlpha Carbon Calculator Demo Launcher
Starts the API server and opens the executive demo in the browser
"""
import uvicorn
import webbrowser
import time
import threading
import sys
import os

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:8000/demo/')
    print("\n🌍 GreenAlpha Carbon Calculator Demo opened in your browser!")
    print("📊 Access the calculator at: http://localhost:8000/demo/")
    print("📖 API documentation: http://localhost:8000/docs")
    print("❤️  Health check: http://localhost:8000/health")
    print("\n💡 Press Ctrl+C to stop the server")

if __name__ == "__main__":
    print("🚀 Starting GreenAlpha Carbon Calculator Demo...")
    print("🔧 Initializing API server...")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for demo
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 GreenAlpha Carbon Calculator Demo stopped!")
        print("Thank you for using GreenAlpha!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)