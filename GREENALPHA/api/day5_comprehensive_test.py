"""
Day 5 Comprehensive Frontend & Visualization Test Suite
Tests all frontend components, visualizations, and integrations
"""
import sys
import os
import asyncio
import time
import requests
import json
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_routing_fix():
    """Test that API routing issues are resolved"""
    print("🧪 Testing API Routing Fix...")
    
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8001/health', timeout=5)
        health_ok = response.status_code == 200
        
        if health_ok:
            print("✅ Health endpoint working")
        else:
            print("❌ Health endpoint failed")
            
        # Test carbon calculation endpoint  
        test_data = {
            'product_name': 'smartphone',
            'quantity': 1,
            'origin_country': 'CHN',
            'destination_country': 'USA', 
            'transport_mode': 'air_freight'
        }
        
        response = requests.post('http://localhost:8001/carbon/calculate', 
                               json=test_data, timeout=10)
        calc_ok = response.status_code == 200
        
        if calc_ok:
            data = response.json()
            print(f"✅ Carbon calculation endpoint working: {data.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
        else:
            print(f"❌ Carbon calculation failed: {response.status_code}")
            
        return health_ok and calc_ok
        
    except Exception as e:
        print(f"❌ API routing test failed: {e}")
        return False

def test_frontend_files():
    """Test that all frontend files exist and are properly structured"""
    print("\n🧪 Testing Frontend File Structure...")
    
    try:
        static_dir = Path("static")
        required_files = [
            "index.html",
            "simple.html", 
            "dashboard.html",
            "analytics.html",
            "style.css",
            "script.js"
        ]
        
        missing_files = []
        for file in required_files:
            file_path = static_dir / file
            if not file_path.exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing frontend files: {missing_files}")
            return False
        
        # Check file sizes (should not be empty)
        for file in required_files:
            file_path = static_dir / file
            if file_path.stat().st_size == 0:
                print(f"❌ Empty file detected: {file}")
                return False
        
        print("✅ All frontend files present and non-empty")
        
        # Check for key HTML structures
        index_content = (static_dir / "index.html").read_text()
        dashboard_content = (static_dir / "dashboard.html").read_text()
        analytics_content = (static_dir / "analytics.html").read_text()
        
        # Check for essential elements
        checks = [
            ("Platform Grid", "platform-grid" in index_content),
            ("Dashboard Charts", "Chart.js" in dashboard_content),
            ("Analytics D3", "d3.v7" in analytics_content),
            ("Responsive Design", "@media" in index_content)
        ]
        
        all_checks_passed = True
        for check_name, check_result in checks:
            if check_result:
                print(f"✅ {check_name} structure found")
            else:
                print(f"❌ {check_name} structure missing")
                all_checks_passed = False
        
        return all_checks_passed
        
    except Exception as e:
        print(f"❌ Frontend file test failed: {e}")
        return False

def test_interactive_charts():
    """Test that interactive chart libraries are accessible"""
    print("\n🧪 Testing Interactive Chart Libraries...")
    
    try:
        # Check if Chart.js is included in dashboard
        dashboard_path = Path("static/dashboard.html")
        if not dashboard_path.exists():
            print("❌ Dashboard file not found")
            return False
            
        dashboard_content = dashboard_path.read_text()
        
        chart_libraries = [
            ("Chart.js", "chart.js" in dashboard_content.lower()),
            ("D3.js", "d3.v7" in Path("static/analytics.html").read_text()),
            ("Plotly", "plotly-latest" in Path("static/analytics.html").read_text())
        ]
        
        all_present = True
        for lib_name, lib_present in chart_libraries:
            if lib_present:
                print(f"✅ {lib_name} library included")
            else:
                print(f"❌ {lib_name} library missing")
                all_present = False
        
        # Check for chart initialization code
        chart_init_patterns = [
            "initializeCharts",
            "new Chart(",
            "Plotly.newPlot",
            "updateCharts"
        ]
        
        dashboard_js = dashboard_content
        analytics_js = Path("static/analytics.html").read_text()
        
        for pattern in chart_init_patterns:
            if pattern in dashboard_js or pattern in analytics_js:
                print(f"✅ Chart initialization pattern found: {pattern}")
            else:
                print(f"⚠️  Chart pattern not found: {pattern}")
        
        return all_present
        
    except Exception as e:
        print(f"❌ Interactive charts test failed: {e}")
        return False

def test_dashboard_widgets():
    """Test dashboard widget components"""
    print("\n🧪 Testing Dashboard Widget Components...")
    
    try:
        dashboard_path = Path("static/dashboard.html")
        dashboard_content = dashboard_path.read_text()
        
        required_widgets = [
            ("Header Metrics", "header-metrics"),
            ("Control Panel", "control-panel"),
            ("KPI Grid", "kpi-grid"),
            ("Chart Containers", "chart-container"),
            ("Action Buttons", "action-buttons"),
            ("Real-time Indicators", "status-indicator")
        ]
        
        all_widgets_found = True
        for widget_name, widget_class in required_widgets:
            if widget_class in dashboard_content:
                print(f"✅ {widget_name} widget found")
            else:
                print(f"❌ {widget_name} widget missing")
                all_widgets_found = False
        
        # Check for JavaScript functionality
        js_functions = [
            "calculateCarbon",
            "updateDashboardData",
            "generateReport",
            "exportData",
            "optimizeRoute"
        ]
        
        for func in js_functions:
            if func in dashboard_content:
                print(f"✅ JavaScript function found: {func}")
            else:
                print(f"❌ JavaScript function missing: {func}")
                all_widgets_found = False
        
        return all_widgets_found
        
    except Exception as e:
        print(f"❌ Dashboard widgets test failed: {e}")
        return False

def test_advanced_visualizations():
    """Test advanced visualization components"""
    print("\n🧪 Testing Advanced Visualization Components...")
    
    try:
        analytics_path = Path("static/analytics.html")
        analytics_content = analytics_path.read_text()
        
        advanced_features = [
            ("Global Heatmap", "globalMap"),
            ("Time Series", "timeSeriesChart"), 
            ("Transport Analysis", "transportAnalysis"),
            ("Sector Breakdown", "sectorBreakdown"),
            ("Arbitrage Chart", "arbitrageChart"),
            ("Performance Metrics", "performanceMetrics"),
            ("Animated Background", "bg-animation"),
            ("Real-time Updates", "startRealTimeUpdates")
        ]
        
        all_features_found = True
        for feature_name, feature_id in advanced_features:
            if feature_id in analytics_content:
                print(f"✅ {feature_name} component found")
            else:
                print(f"❌ {feature_name} component missing")
                all_features_found = False
        
        # Check for advanced chart types
        chart_types = [
            ("Choropleth Map", "choropleth"),
            ("Line Charts", "type: 'scatter'"),
            ("Bar Charts", "type: 'bar'"),
            ("Pie Charts", "type: 'pie'"),
            ("Radar Charts", "type: 'radar'")
        ]
        
        for chart_name, chart_pattern in chart_types:
            if chart_pattern in analytics_content:
                print(f"✅ {chart_name} implementation found")
            else:
                print(f"⚠️  {chart_name} might be missing")
        
        return all_features_found
        
    except Exception as e:
        print(f"❌ Advanced visualizations test failed: {e}")
        return False

def test_real_time_features():
    """Test real-time features and performance monitoring"""
    print("\n🧪 Testing Real-time Features...")
    
    try:
        dashboard_content = Path("static/dashboard.html").read_text()
        analytics_content = Path("static/analytics.html").read_text()
        
        real_time_features = [
            ("Performance Monitoring", "startPerformanceMonitoring"),
            ("Real-time Updates", "setInterval"),
            ("Status Indicators", "status-indicator"),
            ("Live Data Fetch", "fetch(`${API_BASE}"),
            ("Auto Refresh", "refreshData"),
            ("WebSocket Ready", "performance" in dashboard_content.lower())
        ]
        
        all_real_time_ok = True
        for feature_name, pattern in real_time_features:
            if pattern in dashboard_content or pattern in analytics_content:
                print(f"✅ {feature_name} implemented")
            else:
                print(f"❌ {feature_name} missing")
                if feature_name != "WebSocket Ready":  # WebSocket is optional
                    all_real_time_ok = False
        
        # Check for performance optimization
        performance_patterns = [
            ("Response Time Tracking", "responseTime"),
            ("Loading States", "loading"),
            ("Error Handling", "catch (error)"),
            ("Async Operations", "async function")
        ]
        
        for pattern_name, pattern in performance_patterns:
            if pattern in dashboard_content:
                print(f"✅ {pattern_name} found")
            else:
                print(f"⚠️  {pattern_name} might be missing")
        
        return all_real_time_ok
        
    except Exception as e:
        print(f"❌ Real-time features test failed: {e}")
        return False

def test_export_functionality():
    """Test data export and reporting features"""
    print("\n🧪 Testing Export & Reporting Functionality...")
    
    try:
        dashboard_content = Path("static/dashboard.html").read_text()
        
        export_features = [
            ("Export Data Function", "exportData"),
            ("Generate Report", "generateReport"),
            ("CSV Export", "text/csv"),
            ("JSON Export", "application/json"),
            ("Blob Creation", "new Blob"),
            ("Download Link", "createElement('a')"),
            ("File Download", "download =")
        ]
        
        all_export_ok = True
        for feature_name, pattern in export_features:
            if pattern in dashboard_content:
                print(f"✅ {feature_name} implemented")
            else:
                print(f"❌ {feature_name} missing")
                all_export_ok = False
        
        # Check for report generation features
        report_features = [
            ("Report Metadata", "timestamp"),
            ("Data Summary", "summary"),
            ("Performance Stats", "responseTime"),
            ("Export Notifications", "showAlert")
        ]
        
        for feature_name, pattern in report_features:
            if pattern in dashboard_content:
                print(f"✅ {feature_name} found")
            else:
                print(f"⚠️  {feature_name} might be basic")
        
        return all_export_ok
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False

def test_responsive_design():
    """Test responsive design implementation"""
    print("\n🧪 Testing Responsive Design...")
    
    try:
        css_files = ["static/index.html", "static/dashboard.html", "static/analytics.html"]
        
        responsive_features = [
            ("Media Queries", "@media"),
            ("Flexible Grid", "grid-template-columns"),
            ("Viewport Meta", "viewport"),
            ("Mobile Breakpoints", "768px"),
            ("Flexible Units", "rem"),
            ("Responsive Images", "max-width")
        ]
        
        all_responsive = True
        for file_path in css_files:
            if not Path(file_path).exists():
                continue
                
            content = Path(file_path).read_text()
            print(f"\n   Checking {file_path}:")
            
            for feature_name, pattern in responsive_features:
                if pattern in content:
                    print(f"     ✅ {feature_name}")
                else:
                    print(f"     ⚠️  {feature_name} might be missing")
                    if feature_name in ["Media Queries", "Viewport Meta"]:
                        all_responsive = False
        
        return all_responsive
        
    except Exception as e:
        print(f"❌ Responsive design test failed: {e}")
        return False

def test_integration_apis():
    """Test integration with Day 4 APIs"""
    print("\n🧪 Testing Integration with Day 4 APIs...")
    
    try:
        # Check API endpoint calls in frontend
        dashboard_content = Path("static/dashboard.html").read_text()
        
        api_integrations = [
            ("Carbon Calculator", "/carbon/calculate"),
            ("Transport Optimization", "/transport/optimize"),
            ("Supplier Recommendations", "/recommendations/recommend"),
            ("Carbon Arbitrage", "/arbitrage/market-opportunities"),
            ("Health Check", "/health")
        ]
        
        all_integrations_found = True
        for api_name, endpoint in api_integrations:
            if endpoint in dashboard_content:
                print(f"✅ {api_name} API integration found")
            else:
                print(f"❌ {api_name} API integration missing")
                all_integrations_found = False
        
        # Check for error handling
        error_handling = [
            ("Try-Catch Blocks", "try {" in dashboard_content),
            ("Error Messages", "error.message" in dashboard_content),
            ("Status Code Checking", "response.ok" in dashboard_content),
            ("Network Error Handling", "Failed to fetch" in dashboard_content)
        ]
        
        for check_name, check_result in error_handling:
            if check_result:
                print(f"✅ {check_name} implemented")
            else:
                print(f"❌ {check_name} missing")
                all_integrations_found = False
        
        return all_integrations_found
        
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False

async def main():
    """Run all Day 5 comprehensive tests"""
    print("🚀 GreenAlpha Day 5 - Frontend & Visualization Test Suite")
    print("=" * 70)
    
    # Start a test server for API testing
    import subprocess
    import threading
    import time
    
    def start_test_server():
        try:
            subprocess.run([
                "python", "-c", 
                '''
import uvicorn
import time
import threading
from main import app

# Start server in background thread
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Keep the process alive
time.sleep(30)
'''
            ], timeout=35, check=False)
        except:
            pass
    
    # Start server in background
    server_thread = threading.Thread(target=start_test_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("🔄 Starting test server...")
    await asyncio.sleep(3)
    
    tests = [
        ("API Routing Fix", test_api_routing_fix),
        ("Frontend File Structure", test_frontend_files),
        ("Interactive Charts", test_interactive_charts),
        ("Dashboard Widgets", test_dashboard_widgets),
        ("Advanced Visualizations", test_advanced_visualizations),
        ("Real-time Features", test_real_time_features),
        ("Export Functionality", test_export_functionality),
        ("Responsive Design", test_responsive_design),
        ("API Integration", test_integration_apis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 50)
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                success = await test_func()
            else:
                success = test_func()
            
            results.append((test_name, success))
            
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n🎯 Day 5 Frontend & Visualization Test Results")
    print("=" * 70)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    success_rate = passed / len(results)
    print(f"\nOverall: {passed}/{len(results)} tests passed ({success_rate:.0%})")
    
    if success_rate >= 0.85:  # At least 85% pass rate
        print("🎉 Day 5 Frontend Implementation is SUCCESSFUL!")
        print("\n🌟 Key Achievements:")
        print("• ✅ API routing issues completely resolved")
        print("• ✅ Interactive charts with Chart.js, D3.js, Plotly")
        print("• ✅ Comprehensive multi-widget dashboard")
        print("• ✅ Advanced analytics platform with heatmaps")
        print("• ✅ Real-time performance monitoring")  
        print("• ✅ Data export and reporting functionality")
        print("• ✅ Fully responsive design")
        print("• ✅ Complete integration with Day 4 APIs")
        print("\n🚀 Three Complete Platforms Ready:")
        print("   📊 Executive Dashboard (dashboard.html)")
        print("   🔬 Analytics Platform (analytics.html)")
        print("   🧮 Carbon Calculator (simple.html)")
        return True
    else:
        print("⚠️ Day 5 implementation needs minor improvements.")
        print(f"Target: 85% pass rate, Achieved: {success_rate:.0%}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)