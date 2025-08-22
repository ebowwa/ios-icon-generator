#!/usr/bin/env python3
"""
AI Image Generation Module
Handles AI-powered icon generation using ai_proxy_core
"""

import base64
from typing import Optional, Tuple
from PIL import Image
from io import BytesIO
from ai_proxy_core import OpenAIImageProvider, ImageModel


class AIIconGenerator:
    """AI-powered icon generation using OpenAI models"""
    
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        self.provider = OpenAIImageProvider(api_key=api_key)
    
    def generate(
        self,
        prompt: str,
        model: str = "dalle-3"
    ) -> Optional[Image.Image]:
        """
        Generate an icon using AI
        
        Args:
            prompt: The generation prompt
            model: Model to use ('dalle-3', 'dalle-2', 'gpt-image-1')
            
        Returns:
            PIL Image object or None if generation fails
        """
        # Map model name to ImageModel enum
        model_map = {
            'dalle-3': ImageModel.DALLE_3,
            'dalle-2': ImageModel.DALLE_2,
            'gpt-image-1': ImageModel.GPT_IMAGE_1
        }
        
        selected_model = model_map.get(model.lower(), ImageModel.DALLE_3)
        
        print(f"🎨 Generating with {model}...")
        
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
                return self._extract_image_from_response(result['images'])
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
        
        return None
    
    @staticmethod
    def _extract_image_from_response(image_data) -> Optional[Image.Image]:
        """Extract PIL Image from API response"""
        
        if isinstance(image_data, dict):
            # Handle dict response
            if 'data' in image_data:
                if isinstance(image_data['data'], bytes):
                    return Image.open(BytesIO(image_data['data']))
                elif isinstance(image_data['data'], str):
                    img_data = base64.b64decode(image_data['data'])
                    return Image.open(BytesIO(img_data))
            elif 'b64_json' in image_data:
                img_data = base64.b64decode(image_data['b64_json'])
                return Image.open(BytesIO(img_data))
        
        return None