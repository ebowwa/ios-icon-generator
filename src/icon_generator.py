#!/usr/bin/env python3
"""
iOS Icon Generator v2 - Refactored with SRP and Localization Support
Uses modular architecture with proper separation of concerns
"""

import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv

from .ai_generator import AIIconGenerator
from .image_processor import IOSIconProcessor
from .prompt_builder import IconPromptBuilder
from .ios_localization_reader import IOSLocalizationReader


class IconGenerator:
    """Orchestrator for icon generation with modular architecture"""
    
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
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.ai_generator = AIIconGenerator(api_key)
        self.icon_processor = IOSIconProcessor()
        self.prompt_builder = IconPromptBuilder()
    
    def generate_icon(
        self,
        app_name: str,
        colors: Tuple[str, str],
        output_dir: Path,
        style: str = "minimalist",
        model: str = "dalle-3",
        app_description: str = "",
        icon_elements: List[str] = None,
        target_audience: str = "",
        locale: str = "en",
        cultural_style: str = "",
        ios_project_path: Optional[Path] = None,
        additional_prompt: str = ""
    ) -> bool:
        """
        Generate a single icon with full context
        
        Args:
            app_name: Name of the app
            colors: Gradient colors tuple
            output_dir: Where to save the icon
            style: Design style
            model: AI model to use
            app_description: App description
            icon_elements: Visual elements to include
            target_audience: Target audience
            locale: Language/region code
            cultural_style: Cultural design preferences
            ios_project_path: Path to iOS project for localization
            additional_prompt: Additional requirements
            
        Returns:
            True if successful, False otherwise
        """
        # Build prompt with all context
        prompt = self.prompt_builder.build_prompt(
            app_name=app_name,
            colors=colors,
            style=style,
            app_description=app_description,
            icon_elements=icon_elements,
            target_audience=target_audience,
            locale=locale,
            cultural_style=cultural_style,
            ios_project_path=ios_project_path,
            additional_prompt=additional_prompt
        )
        
        print(f"\n📱 Generating icon for: {app_name} ({locale})")
        
        # Generate the image
        image = self.ai_generator.generate(prompt, model)
        
        if image:
            # Save as iOS icon set
            name_prefix = f"AppIcon-{locale}" if locale != "en" else "AppIcon"
            success = self.icon_processor.save_ios_iconset(
                image=image,
                output_dir=output_dir,
                name_prefix=name_prefix
            )
            return success
        
        return False
    
    def generate_from_ios_project(
        self,
        ios_project_path: Path,
        output_dir: Path,
        colors: Tuple[str, str] = ('#1E3A8A', '#60A5FA'),
        style: str = "minimalist",
        model: str = "dalle-3",
        icon_elements: List[str] = None,
        target_audience: str = ""
    ) -> Dict[str, bool]:
        """
        Generate icons for all localizations in an iOS project
        
        Args:
            ios_project_path: Path to iOS project
            output_dir: Where to save icons
            colors: Default gradient colors
            style: Design style
            model: AI model to use
            icon_elements: Visual elements to include
            target_audience: Target audience
            
        Returns:
            Dictionary of locale -> success status
        """
        results = {}
        
        # Find all localizations
        locales = IOSLocalizationReader.find_all_localizations(ios_project_path)
        
        if not locales:
            print("⚠️  No localizations found, generating default icon")
            locales = ['en']
        
        print(f"\n🌍 Found {len(locales)} localizations: {', '.join(locales)}")
        
        for locale in locales:
            # Get localized context
            context = IOSLocalizationReader.get_app_context_from_project(
                ios_project_path, locale
            )
            
            app_name = context.get('display_name') or context.get('app_name') or 'App'
            
            # Generate icon for this locale
            success = self.generate_icon(
                app_name=app_name,
                colors=colors,
                output_dir=output_dir,
                style=style,
                model=model,
                app_description=context.get('description', ''),
                icon_elements=icon_elements,
                target_audience=target_audience,
                locale=locale,
                ios_project_path=ios_project_path
            )
            
            results[locale] = success
        
        return results


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate iOS icons with localization support')
    parser.add_argument('--project', type=Path, help='Path to iOS project')
    parser.add_argument('--name', help='App name (if not using project)')
    parser.add_argument('--output', type=Path, default=Path('./icons'), help='Output directory')
    parser.add_argument('--colors', nargs=2, default=['#1E3A8A', '#60A5FA'], help='Gradient colors')
    parser.add_argument('--style', default='minimalist', help='Design style')
    parser.add_argument('--model', default='dalle-3', help='AI model')
    parser.add_argument('--elements', nargs='+', help='Visual elements')
    parser.add_argument('--audience', help='Target audience')
    parser.add_argument('--locale', default='en', help='Locale (if not using project)')
    
    args = parser.parse_args()
    
    try:
        generator = IconGenerator()
        
        if args.project and args.project.exists():
            # Generate from iOS project
            print(f"📂 Using iOS project: {args.project}")
            results = generator.generate_from_ios_project(
                ios_project_path=args.project,
                output_dir=args.output,
                colors=tuple(args.colors),
                style=args.style,
                model=args.model,
                icon_elements=args.elements,
                target_audience=args.audience or ''
            )
            
            # Summary
            successful = [k for k, v in results.items() if v]
            failed = [k for k, v in results.items() if not v]
            
            print(f"\n✅ Successful: {len(successful)}/{len(results)}")
            if failed:
                print(f"❌ Failed: {', '.join(failed)}")
        
        elif args.name:
            # Generate single icon
            success = generator.generate_icon(
                app_name=args.name,
                colors=tuple(args.colors),
                output_dir=args.output,
                style=args.style,
                model=args.model,
                icon_elements=args.elements,
                target_audience=args.audience or '',
                locale=args.locale
            )
            
            if success:
                print("✅ Icon generated successfully!")
            else:
                print("❌ Failed to generate icon")
        
        else:
            print("Please provide either --project or --name")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())