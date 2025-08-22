#!/usr/bin/env python3
"""
Prompt Builder Module
Constructs AI prompts with rich context including localization
"""

from typing import Dict, List, Tuple, Optional
from pathlib import Path
from ios_localization_reader import IOSLocalizationReader


class IconPromptBuilder:
    """Build rich prompts for icon generation"""
    
    # Locale-specific design context
    CULTURAL_CONTEXTS = {
        'en': 'American/International design aesthetic',
        'en-US': 'American design with Silicon Valley tech aesthetic',
        'en-GB': 'British design with elegant minimalism',
        'ja': 'Japanese design with attention to harmony and minimalism (wa aesthetic)',
        'ko': 'Korean modern K-design aesthetic with soft gradients',
        'zh-Hans': 'Simplified Chinese modern style with contemporary elements',
        'zh-Hant': 'Traditional Chinese elegant style with cultural depth',
        'es': 'Spanish warm and inviting design',
        'es-MX': 'Mexican vibrant and colorful style',
        'fr': 'French elegant and sophisticated design',
        'de': 'German precise and functional design (Bauhaus influence)',
        'it': 'Italian stylish and artistic design',
        'pt-BR': 'Brazilian lively and energetic design',
        'ar': 'Arabic elegant design with right-to-left consideration',
        'ru': 'Russian bold and impactful design',
        'nl': 'Dutch clean and practical design',
        'sv': 'Swedish minimalist Scandinavian design',
        'da': 'Danish hygge-inspired cozy design',
        'fi': 'Finnish functional Nordic design',
        'no': 'Norwegian nature-inspired minimalism',
        'pl': 'Polish traditional meets modern design',
        'tr': 'Turkish blend of Eastern and Western aesthetics',
        'he': 'Hebrew modern design with right-to-left layout',
        'hi': 'Hindi vibrant Indian aesthetic',
        'th': 'Thai ornate and detailed design',
        'vi': 'Vietnamese balanced and harmonious design'
    }
    
    @staticmethod
    def build_prompt(
        app_name: str,
        colors: Tuple[str, str],
        style: str = "minimalist",
        app_description: str = "",
        icon_elements: List[str] = None,
        target_audience: str = "",
        locale: str = "en",
        cultural_style: str = "",
        ios_project_path: Optional[Path] = None,
        additional_prompt: str = ""
    ) -> str:
        """
        Build a comprehensive prompt with all context
        
        Args:
            app_name: Name of the app
            colors: Tuple of (top_color, bottom_color) for gradient
            style: Design style (minimalist, modern, etc.)
            app_description: Description of what the app does
            icon_elements: List of visual elements to include
            target_audience: Target audience description
            locale: Language/region code
            cultural_style: Override for cultural design preferences
            ios_project_path: Path to iOS project for localization context
            additional_prompt: Additional requirements
            
        Returns:
            Complete prompt string
        """
        
        # Get localization context if iOS project path provided
        localization_context = {}
        if ios_project_path and ios_project_path.exists():
            localization_context = IOSLocalizationReader.get_app_context_from_project(
                ios_project_path, locale
            )
            
            # Use localized app name if available
            if localization_context.get('display_name'):
                app_name = localization_context['display_name']
            elif localization_context.get('app_name'):
                app_name = localization_context['app_name']
        
        # Start building the prompt
        prompt = f"""Create a {style} iOS app icon for "{app_name}"

TECHNICAL SPECIFICATIONS:
- Size: 1024x1024 pixel perfect square
- Background: Smooth vertical gradient from {colors[0]} (top) to {colors[1]} (bottom)
- Format: Full bleed to edges, no rounded corners (iOS adds these automatically)
- Style: {style} design with no 3D effects or excessive shadows
- Quality: Professional App Store ready icon
"""
        
        # Add app context
        if app_description:
            prompt += f"\nAPP CONTEXT:\n- Purpose: {app_description}"
        elif localization_context.get('description'):
            prompt += f"\nAPP CONTEXT:\n- Purpose: {localization_context['description']}"
        
        if target_audience:
            prompt += f"\n- Target Audience: {target_audience}"
        
        if localization_context.get('category'):
            prompt += f"\n- Category: {localization_context['category']}"
        
        # Add localization and cultural context
        prompt += "\nLOCALIZATION:"
        prompt += f"\n- Locale: {locale}"
        
        # Use provided cultural style or default from our context
        if cultural_style:
            prompt += f"\n- Cultural Style: {cultural_style}"
        elif locale in IconPromptBuilder.CULTURAL_CONTEXTS:
            prompt += f"\n- Cultural Style: {IconPromptBuilder.CULTURAL_CONTEXTS[locale]}"
        
        # Add any localized strings as context
        if localization_context.get('localized_strings'):
            key_strings = list(localization_context['localized_strings'].items())[:5]
            if key_strings:
                prompt += "\n- App Context (from localization):"
                for key, value in key_strings:
                    prompt += f"\n  • {key}: {value}"
        
        # Add visual elements
        if icon_elements:
            elements_str = ", ".join(icon_elements)
            prompt += f"\n\nVISUAL ELEMENTS:\nInclude these elements in the design: {elements_str}"
        
        # Add text display guidance
        prompt += f"\n\nTEXT DISPLAY:"
        prompt += f"\n- Primary text: '{app_name}'"
        prompt += "\n- Include text only if it enhances the design and remains legible at small sizes"
        prompt += "\n- For non-Latin scripts, ensure proper character rendering"
        
        # Add any additional requirements
        if additional_prompt:
            prompt += f"\n\nADDITIONAL REQUIREMENTS:\n{additional_prompt}"
        
        return prompt
    
    @staticmethod
    def build_batch_prompts(
        ios_project_path: Path,
        base_config: Dict
    ) -> Dict[str, str]:
        """
        Build prompts for all localizations found in an iOS project
        
        Args:
            ios_project_path: Path to iOS project
            base_config: Base configuration with colors, style, etc.
            
        Returns:
            Dictionary of locale -> prompt mappings
        """
        prompts = {}
        
        # Find all localizations
        locales = IOSLocalizationReader.find_all_localizations(ios_project_path)
        
        for locale in locales:
            # Get localized context
            context = IOSLocalizationReader.get_app_context_from_project(
                ios_project_path, locale
            )
            
            # Build prompt for this locale
            prompt = IconPromptBuilder.build_prompt(
                app_name=context.get('display_name', context.get('app_name', base_config.get('app_name', 'App'))),
                colors=base_config.get('colors', ('#1E3A8A', '#60A5FA')),
                style=base_config.get('style', 'minimalist'),
                app_description=context.get('description', base_config.get('description', '')),
                icon_elements=base_config.get('elements', []),
                target_audience=base_config.get('audience', ''),
                locale=locale,
                ios_project_path=ios_project_path
            )
            
            prompts[locale] = prompt
        
        return prompts