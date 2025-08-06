#!/usr/bin/env python3
"""
GreenAlpha Executive Demo Launcher
Simple script to start the demo for executives
"""
import os
import sys
import time
import webbrowser
import subprocess
import threading
from pathlib import Path

def print_banner():
    """Print demo banner"""
    print("\n" + "="*60)
    print("🌱 GreenAlpha Carbon Calculator - Executive Demo")
    print("="*60)
    print("Starting enterprise-grade carbon footprint calculation demo...")
    print("Target audience: C-level executives and decision makers")
    print("="*60 + "\n")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import uvicorn
        import fastapi
        print("✅ FastAPI and Uvicorn are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\nPlease install dependencies with:")
        print("pip install fastapi uvicorn")
        return False

def start_server():
    """Start the FastAPI server"""
    try:
        # Set environment variables for production-like behavior
        os.environ['PYTHONPATH'] = os.getcwd()
        
        # Start the server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        print("🚀 Starting GreenAlpha API server...")
        print("Server will be available at: http://localhost:8000")
        print("Demo interface will be at: http://localhost:8000/demo")
        print("\nServer logs:")
        print("-" * 40)
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def wait_for_server(timeout=30):
    """Wait for server to be ready"""
    import requests
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def open_demo():
    """Open the demo in the default browser"""
    demo_url = "http://localhost:8000/demo"
    print(f"\n🌐 Opening demo interface: {demo_url}")
    webbrowser.open(demo_url)

def print_demo_info():
    """Print demo information for executives"""
    print("\n" + "="*60)
    print("📊 EXECUTIVE DEMO - READY")
    print("="*60)
    print("\n🎯 DEMO FEATURES:")
    print("  • Real-time carbon footprint calculations (<10ms)")
    print("  • Interactive product scenarios")
    print("  • Business value calculator (ROI analysis)")
    print("  • Performance metrics dashboard")
    print("  • 222 countries, 267 years of data")
    print("  • IPCC 2021 compliant methodology")
    
    print("\n🚀 QUICK START SCENARIOS:")
    print("  1. Smartphone: China → USA (Air freight)")
    print("  2. Laptop: Germany → Japan (Sea freight)")
    print("  3. T-shirt: India → UK (Sea freight)")
    
    print("\n💼 BUSINESS VALUE:")
    print("  • 95% reduction in reporting time")
    print("  • $100K+ annual cost savings potential")
    print("  • Real-time sustainability decisions")
    print("  • Competitive ESG advantage")
    
    print("\n🔗 DEMO ACCESS:")
    print(f"  • Demo Interface: http://localhost:8000/demo")
    print(f"  • API Documentation: http://localhost:8000/docs")
    print(f"  • Health Check: http://localhost:8000/health")
    
    print("\n⏹️  To stop the demo: Press Ctrl+C")
    print("="*60 + "\n")

def main():
    """Main demo launcher"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Please run this script from the API directory")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start the server
    server_process = start_server()
    if not server_process:
        sys.exit(1)
    
    try:
        # Wait a moment for server to start
        print("\n⏳ Waiting for server to initialize...")
        time.sleep(3)
        
        # Try to check if server is ready
        try:
            import requests
            if wait_for_server():
                print("✅ Server is ready!")
                open_demo()
                print_demo_info()
            else:
                print("⚠️  Server may still be starting up...")
                print("Demo will be available at: http://localhost:8000/demo")
        except ImportError:
            print("ℹ️  Install 'requests' for automatic health checks: pip install requests")
            time.sleep(2)
            open_demo()
            print_demo_info()
        
        # Keep the demo running
        print("Demo is running... Press Ctrl+C to stop")
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping demo...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✅ Demo stopped successfully")
    
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()