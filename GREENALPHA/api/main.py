"""
GreenAlpha Carbon Footprint Engine - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from datetime import datetime
import asyncio
import os

# Import routes
from api.routes.carbon_calculator import router as carbon_router
from api.routes.recommendations import router as recommendations_router
from api.routes.transport_optimization import router as transport_router
from api.routes.carbon_arbitrage import router as arbitrage_router

# Import core components for initialization
from api.core.data_access import data_manager
from api.core.carbon_engine import carbon_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="GreenAlpha Carbon Footprint Engine",
    description="Advanced carbon footprint calculation and sustainability analytics API with <500ms response time",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(carbon_router, prefix="/carbon", tags=["Carbon Calculation"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["Supplier Recommendations"])
app.include_router(transport_router, prefix="/transport", tags=["Transport Optimization"])
app.include_router(arbitrage_router, prefix="/arbitrage", tags=["Carbon Arbitrage"])

# Mount static files for the demo frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.mount("/demo", StaticFiles(directory=static_dir, html=True), name="demo")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Restricted to local development
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only required methods
    allow_headers=["Content-Type", "Authorization"],  # Only required headers
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.utcnow().isoformat()}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Ensure data manager is initialized
        await data_manager.ensure_initialized()
        
        # Check data manager
        data_stats = data_manager.get_performance_stats()
        engine_stats = carbon_engine.get_performance_stats()
        
        # Basic health indicators
        is_healthy = (
            data_stats["countries_loaded"] > 0 and
            data_stats["data_size"] > 0
        )
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "GreenAlpha Carbon Footprint Engine",
            "version": "1.0.0",
            "components": {
                "data_manager": {
                    "status": "healthy" if data_stats["countries_loaded"] > 0 else "error",
                    "countries_loaded": data_stats["countries_loaded"],
                    "data_records": data_stats["data_size"]
                },
                "calculation_engine": {
                    "status": "healthy",
                    "avg_response_time": engine_stats.get("avg_response_time_ms", 0),
                    "total_calculations": engine_stats.get("total_calculations", 0)
                }
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "GreenAlpha Carbon Footprint Engine",
            "version": "1.0.0",
            "error": str(e)
        }

# Application startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application components on startup"""
    logger.info("Starting GreenAlpha Carbon Footprint Engine...")
    try:
        # Initialize data manager properly
        await data_manager.ensure_initialized()
        logger.info("Carbon calculation engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Shutting down GreenAlpha Carbon Footprint Engine...")

# Root endpoint - redirect to demo
@app.get("/")
async def root():
    """Root endpoint - redirect to demo"""
    return RedirectResponse(url="/demo/", status_code=307)

# API info endpoint
@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Welcome to GreenAlpha Carbon Footprint Engine",
        "description": "Production-ready carbon footprint calculation API",
        "features": [
            "<500ms response time",
            "95%+ calculation accuracy",
            "IPCC 2021 methodology",
            "Global coverage",
            "Real-time carbon pricing"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "demo": "/demo",
            "carbon_calculator": "/carbon/calculate",
            "batch_calculator": "/carbon/calculate/batch",
            "global_stats": "/carbon/stats/global",
            "supplier_recommendations": "/recommendations/recommend/suppliers",
            "transport_optimization": "/transport/optimize/route",
            "carbon_arbitrage": "/arbitrage/comprehensive-report"
        },
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )