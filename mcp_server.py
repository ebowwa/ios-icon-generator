#!/usr/bin/env python3
"""
MCP Server for iOS Icon Generator
Model Context Protocol server for AI-powered icon generation
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.icon_generator import IconGenerator
from src.ios_localization_reader import IOSLocalizationReader
from src.prompt_builder import IconPromptBuilder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global generator instance
_generator = None


def get_generator() -> IconGenerator:
    """Get or create the icon generator instance"""
    global _generator
    if _generator is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        _generator = IconGenerator(api_key)
    return _generator


async def main():
    """Main MCP server entry point"""
    
    # Create server instance
    server = Server("ios-icon-generator")
    
    # Tool 1: Generate Icon
    @server.list_tools()
    async def list_tools():
        """List available tools"""
        return [
            {
                "name": "generate_icon",
                "description": "Generate a single iOS app icon with AI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "Name of the app"
                        },
                        "colors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Gradient colors [top, bottom] in hex format",
                            "default": ["#1E3A8A", "#60A5FA"]
                        },
                        "style": {
                            "type": "string",
                            "description": "Design style (minimalist, modern, etc.)",
                            "default": "minimalist"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["dalle-3", "dalle-2", "gpt-image-1"],
                            "description": "AI model to use",
                            "default": "dalle-3"
                        },
                        "app_description": {
                            "type": "string",
                            "description": "Description of what the app does"
                        },
                        "icon_elements": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Visual elements to include in the icon"
                        },
                        "target_audience": {
                            "type": "string",
                            "description": "Target audience for the app"
                        },
                        "locale": {
                            "type": "string",
                            "description": "Language/region code (e.g., en, ja, es)",
                            "default": "en"
                        },
                        "cultural_style": {
                            "type": "string",
                            "description": "Cultural design preferences"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Output directory path",
                            "default": "./generated_icons"
                        }
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "generate_from_project",
                "description": "Generate icons for all localizations in an iOS project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ios_project_path": {
                            "type": "string",
                            "description": "Path to the iOS project directory"
                        },
                        "colors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Gradient colors [top, bottom]",
                            "default": ["#1E3A8A", "#60A5FA"]
                        },
                        "style": {
                            "type": "string",
                            "description": "Design style",
                            "default": "minimalist"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["dalle-3", "dalle-2", "gpt-image-1"],
                            "description": "AI model to use",
                            "default": "dalle-3"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Output directory",
                            "default": "./generated_icons"
                        }
                    },
                    "required": ["ios_project_path"]
                }
            },
            {
                "name": "get_localizations",
                "description": "Get all available localizations from an iOS project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ios_project_path": {
                            "type": "string",
                            "description": "Path to the iOS project directory"
                        }
                    },
                    "required": ["ios_project_path"]
                }
            },
            {
                "name": "list_cultural_styles",
                "description": "List available cultural design styles for different locales",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    # Tool handler
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list:
        """Handle tool calls"""
        
        if name == "generate_icon":
            try:
                generator = get_generator()
                output_path = Path(arguments.get("output_dir", "./generated_icons"))
                output_path.mkdir(parents=True, exist_ok=True)
                
                # Convert colors list to tuple
                colors = arguments.get("colors", ["#1E3A8A", "#60A5FA"])
                color_tuple = tuple(colors)
                
                success = generator.generate_icon(
                    app_name=arguments["app_name"],
                    colors=color_tuple,
                    output_dir=output_path,
                    style=arguments.get("style", "minimalist"),
                    model=arguments.get("model", "dalle-3"),
                    app_description=arguments.get("app_description", ""),
                    icon_elements=arguments.get("icon_elements", []),
                    target_audience=arguments.get("target_audience", ""),
                    locale=arguments.get("locale", "en"),
                    cultural_style=arguments.get("cultural_style", "")
                )
                
                if success:
                    locale = arguments.get("locale", "en")
                    iconset_path = output_path / f"AppIcon-{locale}.appiconset"
                    preview_path = output_path / f"AppIcon-{locale}_preview.png"
                    
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "success": True,
                            "message": f"Icon generated successfully for {arguments['app_name']}",
                            "iconset_path": str(iconset_path),
                            "preview_path": str(preview_path),
                            "locale": locale
                        }, indent=2)
                    }]
                else:
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "success": False,
                            "error": "Failed to generate icon"
                        }, indent=2)
                    }]
                    
            except Exception as e:
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "success": False,
                        "error": str(e)
                    }, indent=2)
                }]
        
        elif name == "generate_from_project":
            try:
                generator = get_generator()
                project_path = Path(arguments["ios_project_path"])
                
                if not project_path.exists():
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "success": False,
                            "error": f"Project path does not exist: {arguments['ios_project_path']}"
                        }, indent=2)
                    }]
                
                output_path = Path(arguments.get("output_dir", "./generated_icons"))
                output_path.mkdir(parents=True, exist_ok=True)
                
                colors = arguments.get("colors", ["#1E3A8A", "#60A5FA"])
                color_tuple = tuple(colors)
                
                results = generator.generate_from_ios_project(
                    ios_project_path=project_path,
                    output_dir=output_path,
                    colors=color_tuple,
                    style=arguments.get("style", "minimalist"),
                    model=arguments.get("model", "dalle-3")
                )
                
                successful = [k for k, v in results.items() if v]
                failed = [k for k, v in results.items() if not v]
                
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "success": True,
                        "message": f"Generated icons for {len(successful)}/{len(results)} localizations",
                        "results": results,
                        "successful": successful,
                        "failed": failed,
                        "output_dir": str(output_path)
                    }, indent=2)
                }]
                
            except Exception as e:
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "success": False,
                        "error": str(e)
                    }, indent=2)
                }]
        
        elif name == "get_localizations":
            try:
                project_path = Path(arguments["ios_project_path"])
                
                if not project_path.exists():
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "success": False,
                            "error": f"Project path does not exist: {arguments['ios_project_path']}"
                        }, indent=2)
                    }]
                
                locales = IOSLocalizationReader.find_all_localizations(project_path)
                
                localizations = []
                for locale in locales:
                    context = IOSLocalizationReader.get_app_context_from_project(
                        project_path, locale
                    )
                    localizations.append({
                        "locale": locale,
                        "app_name": context.get('app_name'),
                        "display_name": context.get('display_name'),
                        "description": context.get('description'),
                        "category": context.get('category')
                    })
                
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "success": True,
                        "localizations": localizations,
                        "count": len(localizations)
                    }, indent=2)
                }]
                
            except Exception as e:
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "success": False,
                        "error": str(e)
                    }, indent=2)
                }]
        
        elif name == "list_cultural_styles":
            return [{
                "type": "text",
                "text": json.dumps({
                    "cultural_contexts": IconPromptBuilder.CULTURAL_CONTEXTS,
                    "count": len(IconPromptBuilder.CULTURAL_CONTEXTS)
                }, indent=2)
            }]
        
        else:
            return [{
                "type": "text",
                "text": json.dumps({
                    "success": False,
                    "error": f"Unknown tool: {name}"
                }, indent=2)
            }]
    
    # Run the server
    logger.info("🚀 Starting iOS Icon Generator MCP Server")
    logger.info("📱 Available tools: generate_icon, generate_from_project, get_localizations, list_cultural_styles")
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        logger.warning("⚠️  OPENAI_API_KEY not set in environment")
    
    # Run with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())