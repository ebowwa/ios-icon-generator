#!/usr/bin/env python3
"""
MCP Server for iOS Icon Generator
Exposes icon generation capabilities via FastAPI MCP
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from pathlib import Path
import tempfile
import shutil
import os
from datetime import datetime

from fastapi_mcp import FastApiMCP

from .icon_generator import IconGenerator
from .ios_localization_reader import IOSLocalizationReader

# Initialize FastAPI app
app = FastAPI(
    title="iOS Icon Generator MCP",
    description="AI-powered iOS icon generation with localization support",
    version="2.0.0"
)

# Initialize MCP
mcp = FastApiMCP(app)


# Pydantic models for request/response
class IconGenerationRequest(BaseModel):
    app_name: str = Field(..., description="Name of the app")
    colors: Tuple[str, str] = Field(default=("#1E3A8A", "#60A5FA"), description="Gradient colors (top, bottom)")
    style: str = Field(default="minimalist", description="Design style (minimalist, modern, etc.)")
    model: str = Field(default="dalle-3", description="AI model to use (dalle-3, dalle-2)")
    app_description: Optional[str] = Field(None, description="Description of the app")
    icon_elements: Optional[List[str]] = Field(None, description="Visual elements to include")
    target_audience: Optional[str] = Field(None, description="Target audience")
    locale: str = Field(default="en", description="Language/region code")
    cultural_style: Optional[str] = Field(None, description="Cultural design preferences")
    additional_prompt: Optional[str] = Field(None, description="Additional requirements")


class ProjectIconGenerationRequest(BaseModel):
    ios_project_path: str = Field(..., description="Path to iOS project")
    colors: Tuple[str, str] = Field(default=("#1E3A8A", "#60A5FA"), description="Gradient colors")
    style: str = Field(default="minimalist", description="Design style")
    model: str = Field(default="dalle-3", description="AI model")
    icon_elements: Optional[List[str]] = Field(None, description="Visual elements")
    target_audience: Optional[str] = Field(None, description="Target audience")


class LocalizationInfo(BaseModel):
    locale: str
    app_name: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    category: Optional[str]


class GenerationResult(BaseModel):
    success: bool
    message: str
    output_path: Optional[str]
    preview_url: Optional[str]
    locale: Optional[str]


# Global generator instance (initialized on first use)
_generator = None


def get_generator() -> IconGenerator:
    """Get or create the icon generator instance"""
    global _generator
    if _generator is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
        _generator = IconGenerator(api_key)
    return _generator


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "iOS Icon Generator MCP",
        "version": "2.0.0",
        "endpoints": {
            "generate_icon": "/generate",
            "generate_from_project": "/generate-from-project",
            "get_localizations": "/localizations",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": bool(os.getenv('OPENAI_API_KEY'))
    }


@app.post("/generate", response_model=GenerationResult)
async def generate_icon(
    request: IconGenerationRequest,
    background_tasks: BackgroundTasks
) -> GenerationResult:
    """
    Generate a single iOS icon with specified parameters
    
    This endpoint creates an iOS app icon using AI generation with full customization options.
    """
    try:
        generator = get_generator()
        
        # Create temporary output directory
        output_dir = Path(tempfile.mkdtemp(prefix="icon_gen_"))
        
        # Generate the icon
        success = generator.generate_icon(
            app_name=request.app_name,
            colors=request.colors,
            output_dir=output_dir,
            style=request.style,
            model=request.model,
            app_description=request.app_description or "",
            icon_elements=request.icon_elements or [],
            target_audience=request.target_audience or "",
            locale=request.locale,
            cultural_style=request.cultural_style or "",
            additional_prompt=request.additional_prompt or ""
        )
        
        if success:
            # Schedule cleanup after response
            background_tasks.add_task(cleanup_temp_dir, output_dir, delay=3600)
            
            return GenerationResult(
                success=True,
                message=f"Icon generated successfully for {request.app_name}",
                output_path=str(output_dir),
                preview_url=f"/preview/{output_dir.name}",
                locale=request.locale
            )
        else:
            # Clean up immediately on failure
            shutil.rmtree(output_dir, ignore_errors=True)
            return GenerationResult(
                success=False,
                message="Failed to generate icon",
                output_path=None,
                preview_url=None,
                locale=request.locale
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-from-project", response_model=Dict[str, GenerationResult])
async def generate_from_project(
    request: ProjectIconGenerationRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, GenerationResult]:
    """
    Generate icons for all localizations in an iOS project
    
    Automatically detects all localizations in the project and generates
    culturally-appropriate icons for each locale.
    """
    try:
        generator = get_generator()
        project_path = Path(request.ios_project_path)
        
        if not project_path.exists():
            raise HTTPException(status_code=400, detail=f"Project path does not exist: {request.ios_project_path}")
        
        # Create temporary output directory
        output_dir = Path(tempfile.mkdtemp(prefix="icon_gen_project_"))
        
        # Generate icons for all localizations
        results = generator.generate_from_ios_project(
            ios_project_path=project_path,
            output_dir=output_dir,
            colors=request.colors,
            style=request.style,
            model=request.model,
            icon_elements=request.icon_elements or [],
            target_audience=request.target_audience or ""
        )
        
        # Convert results to response format
        response = {}
        for locale, success in results.items():
            response[locale] = GenerationResult(
                success=success,
                message=f"Icon generated for {locale}" if success else f"Failed to generate for {locale}",
                output_path=str(output_dir / f"AppIcon-{locale}.appiconset") if success else None,
                preview_url=f"/preview/{output_dir.name}/{locale}" if success else None,
                locale=locale
            )
        
        # Schedule cleanup after response
        background_tasks.add_task(cleanup_temp_dir, output_dir, delay=3600)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/localizations/{project_path:path}", response_model=List[LocalizationInfo])
async def get_localizations(project_path: str) -> List[LocalizationInfo]:
    """
    Get all available localizations from an iOS project
    
    Scans the project for .lproj directories and extracts localization information.
    """
    try:
        path = Path(project_path)
        if not path.exists():
            raise HTTPException(status_code=400, detail=f"Project path does not exist: {project_path}")
        
        locales = IOSLocalizationReader.find_all_localizations(path)
        
        if not locales:
            return []
        
        localizations = []
        for locale in locales:
            context = IOSLocalizationReader.get_app_context_from_project(path, locale)
            localizations.append(LocalizationInfo(
                locale=locale,
                app_name=context.get('app_name'),
                display_name=context.get('display_name'),
                description=context.get('description'),
                category=context.get('category')
            ))
        
        return localizations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preview/{temp_id}/{locale}")
async def get_preview(temp_id: str, locale: str):
    """Get preview image for a generated icon"""
    preview_path = Path(tempfile.gettempdir()) / temp_id / f"AppIcon-{locale}_preview.png"
    
    if not preview_path.exists():
        raise HTTPException(status_code=404, detail="Preview not found")
    
    return FileResponse(preview_path, media_type="image/png")


@app.get("/download/{temp_id}")
async def download_iconset(temp_id: str):
    """Download the generated icon set as a zip file"""
    temp_dir = Path(tempfile.gettempdir()) / temp_id
    
    if not temp_dir.exists():
        raise HTTPException(status_code=404, detail="Icon set not found")
    
    # Create zip file
    zip_path = temp_dir / "iconset.zip"
    shutil.make_archive(str(zip_path.with_suffix('')), 'zip', temp_dir)
    
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"ios_icons_{temp_id}.zip"
    )


def cleanup_temp_dir(path: Path, delay: int = 0):
    """Clean up temporary directory after delay"""
    import time
    if delay > 0:
        time.sleep(delay)
    shutil.rmtree(path, ignore_errors=True)


# Mount MCP endpoints
mcp.mount()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)