#!/usr/bin/env python3
"""
Image Processing Module
Handles image manipulation and saving operations
"""

import json
from pathlib import Path
from typing import Dict
from PIL import Image


class IOSIconProcessor:
    """Process and save iOS icon sets"""
    
    # iOS icon sizes specification
    IOS_SIZES = {
        "AppIcon-20@2x.png": 40,
        "AppIcon-20@3x.png": 60,
        "AppIcon-29@2x.png": 58,
        "AppIcon-29@3x.png": 87,
        "AppIcon-40@2x.png": 80,
        "AppIcon-40@3x.png": 120,
        "AppIcon-60@2x.png": 120,
        "AppIcon-60@3x.png": 180,
        "AppIcon-76.png": 76,
        "AppIcon-76@2x.png": 152,
        "AppIcon-83.5@2x.png": 167,
        "AppIcon-1024.png": 1024,
    }
    
    @staticmethod
    def save_ios_iconset(
        image: Image.Image,
        output_dir: Path,
        name_prefix: str = "AppIcon"
    ) -> bool:
        """
        Save icon in all required iOS sizes
        
        Args:
            image: PIL Image object
            output_dir: Directory to save the icon set
            name_prefix: Prefix for the icon set folder
            
        Returns:
            True if successful, False otherwise
        """
        if not image:
            return False
        
        # Create iconset directory
        iconset_dir = output_dir / f"{name_prefix}.appiconset"
        iconset_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure RGBA mode
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        print(f"💾 Saving iOS icon set to {iconset_dir}")
        
        # Generate all required sizes
        for filename, size in IOSIconProcessor.IOS_SIZES.items():
            resized = image.resize((size, size), Image.Resampling.LANCZOS)
            filepath = iconset_dir / filename
            resized.save(filepath, 'PNG', optimize=True)
            print(f"   ✓ {filename} ({size}x{size})")
        
        # Create Contents.json for Xcode
        IOSIconProcessor._create_ios_contents_json(iconset_dir)
        
        # Save preview
        preview_path = output_dir / f"{name_prefix}_preview.png"
        image.save(preview_path, 'PNG')
        print(f"   ✓ Preview saved to {preview_path}")
        
        return True
    
    @staticmethod
    def _create_ios_contents_json(iconset_dir: Path):
        """Create Contents.json file specifically for iOS/Xcode"""
        
        contents = {
            "images": [
                {"filename": "AppIcon-20@2x.png", "idiom": "iphone", "scale": "2x", "size": "20x20"},
                {"filename": "AppIcon-20@3x.png", "idiom": "iphone", "scale": "3x", "size": "20x20"},
                {"filename": "AppIcon-29@2x.png", "idiom": "iphone", "scale": "2x", "size": "29x29"},
                {"filename": "AppIcon-29@3x.png", "idiom": "iphone", "scale": "3x", "size": "29x29"},
                {"filename": "AppIcon-40@2x.png", "idiom": "iphone", "scale": "2x", "size": "40x40"},
                {"filename": "AppIcon-40@3x.png", "idiom": "iphone", "scale": "3x", "size": "40x40"},
                {"filename": "AppIcon-60@2x.png", "idiom": "iphone", "scale": "2x", "size": "60x60"},
                {"filename": "AppIcon-60@3x.png", "idiom": "iphone", "scale": "3x", "size": "60x60"},
                {"filename": "AppIcon-76.png", "idiom": "ipad", "scale": "1x", "size": "76x76"},
                {"filename": "AppIcon-76@2x.png", "idiom": "ipad", "scale": "2x", "size": "76x76"},
                {"filename": "AppIcon-83.5@2x.png", "idiom": "ipad", "scale": "2x", "size": "83.5x83.5"},
                {"filename": "AppIcon-1024.png", "idiom": "ios-marketing", "scale": "1x", "size": "1024x1024"}
            ],
            "info": {
                "author": "xcode",
                "version": 1
            }
        }
        
        with open(iconset_dir / "Contents.json", 'w') as f:
            json.dump(contents, f, indent=2)
        print(f"   ✓ iOS Contents.json")


class WebIconProcessor:
    """Process and save web icons (future enhancement)"""
    
    WEB_SIZES = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "favicon-48.png": 48,
        "favicon-64.png": 64,
        "favicon-128.png": 128,
        "favicon-256.png": 256
    }
    
    @staticmethod
    def save_web_icons(image: Image.Image, output_dir: Path) -> bool:
        """Save web favicon set (to be implemented)"""
        # TODO: Implement web icon generation
        pass