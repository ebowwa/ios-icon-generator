#!/usr/bin/env python3
"""
iOS Icon Generator using ai_proxy_core
Generates all required iOS app icon sizes using AI image generation
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Tuple, Optional
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from ai_proxy_core import OpenAIImageProvider, ImageModel

# Standard iOS icon sizes required for App Store
IOS_ICON_SIZES = {
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


class IconGenerator:
    """iOS Icon Generator using ai_proxy_core"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the icon generator
        
        Args:
            api_key: OpenAI API key (if not provided, will try to load from env)
        """
        if not api_key:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.provider = OpenAIImageProvider(api_key=api_key)
    
    def generate_icon(
        self,
        app_name: str,
        colors: Tuple[str, str],
        style: str = "minimalist",
        model: str = "dalle-3",
        additional_prompt: str = ""
    ) -> Optional[Image.Image]:
        """
        Generate a single app icon
        
        Args:
            app_name: Name of the app to display on icon
            colors: Tuple of (top_color, bottom_color) for gradient
            style: Design style (minimalist, modern, playful, etc.)
            model: AI model to use ('dalle-3', 'dalle-2', or 'gpt-image-1')
            additional_prompt: Additional details for the prompt
            
        Returns:
            PIL Image object or None if generation fails
        """
        # Build the prompt
        prompt = self._build_prompt(app_name, colors, style, additional_prompt)
        
        # Map model name to ImageModel enum
        model_map = {
            'dalle-3': ImageModel.DALLE_3,
            'dalle-2': ImageModel.DALLE_2,
            'gpt-image-1': ImageModel.GPT_IMAGE_1
        }
        
        selected_model = model_map.get(model.lower(), ImageModel.DALLE_3)
        
        print(f"🎨 Generating icon with {model}...")
        print(f"   App: {app_name}")
        print(f"   Colors: {colors[0]} → {colors[1]}")
        
        try:
            # Configure parameters based on model
            params = {
                'model': selected_model,
                'prompt': prompt,
                'size': '1024x1024',
                'n': 1,
                'response_format': 'b64_json'
            }
            
            # Add model-specific parameters
            if selected_model == ImageModel.DALLE_3:
                params['quality'] = 'standard'
                params['style'] = 'natural'
            elif selected_model == ImageModel.GPT_IMAGE_1:
                params['quality'] = 'high'
            
            # Generate the image
            result = self.provider.generate(**params)
            
            if result and 'images' in result:
                return self._extract_image(result['images'])
            
        except Exception as e:
            print(f"❌ Error generating icon: {e}")
        
        return None
    
    def _build_prompt(
        self,
        app_name: str,
        colors: Tuple[str, str],
        style: str,
        additional_prompt: str
    ) -> str:
        """Build the generation prompt"""
        
        base_prompt = f"""Create a {style} iOS app icon with these specifications:
- Size: 1024x1024 pixel perfect square
- Background: Smooth vertical gradient from {colors[0]} (top) to {colors[1]} (bottom)
- Design: Clean, professional app icon suitable for the App Store
- Text: "{app_name}" if it fits naturally in the design
- Style: {style} design with no 3D effects or excessive shadows
- Format: Full bleed to edges, no rounded corners (iOS adds these automatically)
"""
        
        if additional_prompt:
            base_prompt += f"\nAdditional details: {additional_prompt}"
        
        return base_prompt
    
    def _extract_image(self, image_data) -> Optional[Image.Image]:
        """Extract PIL Image from API response"""
        
        if isinstance(image_data, dict):
            # Handle dict response
            if 'data' in image_data:
                if isinstance(image_data['data'], bytes):
                    return Image.open(BytesIO(image_data['data']))
                elif isinstance(image_data['data'], str):
                    import base64
                    img_data = base64.b64decode(image_data['data'])
                    return Image.open(BytesIO(img_data))
            elif 'b64_json' in image_data:
                import base64
                img_data = base64.b64decode(image_data['b64_json'])
                return Image.open(BytesIO(img_data))
        
        return None
    
    def save_icon_set(
        self,
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
        
        print(f"💾 Saving icon set to {iconset_dir}")
        
        # Generate all required sizes
        for filename, size in IOS_ICON_SIZES.items():
            resized = image.resize((size, size), Image.Resampling.LANCZOS)
            filepath = iconset_dir / filename
            resized.save(filepath, 'PNG', optimize=True)
            print(f"   ✓ {filename} ({size}x{size})")
        
        # Create Contents.json for Xcode
        self._create_contents_json(iconset_dir)
        
        # Save preview
        preview_path = output_dir / f"{name_prefix}_preview.png"
        image.save(preview_path, 'PNG')
        print(f"   ✓ Preview saved to {preview_path}")
        
        return True
    
    def _create_contents_json(self, iconset_dir: Path):
        """Create Contents.json file for Xcode"""
        
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
        print(f"   ✓ Contents.json")


def main():
    """CLI interface for the icon generator"""
    
    parser = argparse.ArgumentParser(description='Generate iOS app icons using AI')
    parser.add_argument('app_name', help='Name of the app')
    parser.add_argument('--colors', nargs=2, default=['#1E3A8A', '#60A5FA'],
                       help='Gradient colors (top bottom)')
    parser.add_argument('--style', default='minimalist',
                       choices=['minimalist', 'modern', 'playful', 'professional', 'elegant'],
                       help='Design style')
    parser.add_argument('--model', default='dalle-3',
                       choices=['dalle-3', 'dalle-2', 'gpt-image-1'],
                       help='AI model to use')
    parser.add_argument('--output', type=Path, default=Path.cwd(),
                       help='Output directory')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--additional', default='',
                       help='Additional prompt details')
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = IconGenerator(api_key=args.api_key)
        
        # Generate icon
        image = generator.generate_icon(
            app_name=args.app_name,
            colors=tuple(args.colors),
            style=args.style,
            model=args.model,
            additional_prompt=args.additional
        )
        
        if image:
            # Save icon set
            success = generator.save_icon_set(
                image=image,
                output_dir=args.output,
                name_prefix=f"AppIcon-{args.app_name.replace(' ', '')}"
            )
            
            if success:
                print(f"\n✅ Successfully generated icon set for {args.app_name}")
            else:
                print(f"\n❌ Failed to save icon set")
        else:
            print(f"\n❌ Failed to generate icon")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())