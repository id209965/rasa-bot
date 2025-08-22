from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid
from pathlib import Path

from app.config import settings
from app.database.connection import get_session, init_database, close_database
from app.api.routes import admin, files, maps

app = FastAPI(
    title="Test Bot API",
    description="API для чат-бота Тест",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(maps.router, prefix="/api/maps", tags=["maps"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    await close_database()


@app.get("/")
async def root():
    return {"message": "Test Bot API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
