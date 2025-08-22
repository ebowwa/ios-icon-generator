#!/usr/bin/env python3
"""
Example: Generate localized icons for a Sleep Tracking App with rich context
"""

from icon_generator import IconGenerator
from pathlib import Path
import os


def generate_sleep_app_icons():
    """Generate icons for SleepCycles app with full context"""
    
    # Rich context for the sleep tracking app
    app_context = {
        'description': 'A sleep tracking and analysis app that helps users improve their sleep quality through cycle monitoring, smart alarms, and personalized insights',
        'elements': ['crescent moon', 'stars', 'soft clouds'],
        'audience': 'Health-conscious adults aged 25-45 who want to optimize their sleep patterns'
    }
    
    # Locale-specific configurations with cultural context
    locale_configs = {
        'en': {
            'name': 'SleepLoops',
            'colors': ('#1E3A8A', '#60A5FA'),
            'style': 'minimalist',
            'cultural': 'Clean Silicon Valley tech aesthetic',
            'additional': 'Professional yet approachable design'
        },
        'ja': {
            'name': '睡眠管理',
            'colors': ('#1F2937', '#F59E0B'),
            'style': 'minimalist',
            'cultural': 'Japanese zen philosophy with wa (harmony) aesthetic',
            'additional': 'Incorporate traditional Japanese minimalism with modern functionality'
        },
        'es-MX': {
            'name': 'CiclosSueño',
            'colors': ('#16A34A', '#4ADE80'),
            'style': 'modern',
            'cultural': 'Vibrant Mexican design with warm, inviting colors',
            'additional': 'Blend modern tech with traditional Mexican warmth'
        },
        'ko': {
            'name': '수면사이클',
            'colors': ('#0891B2', '#67E8F9'),
            'style': 'modern',
            'cultural': 'K-design aesthetic with clean lines and soft gradients',
            'additional': 'Modern Korean design language emphasizing clarity and sophistication'
        },
        'zh-Hant': {
            'name': '安眠週期',
            'colors': ('#DC2626', '#FCA5A5'),
            'style': 'elegant',
            'cultural': 'Traditional Chinese elegance with modern twist',
            'additional': 'Balance traditional Chinese symbolism with contemporary app design'
        },
        'ar': {
            'name': 'دورات النوم',
            'colors': ('#059669', '#34D399'),
            'style': 'elegant',
            'cultural': 'Arabic geometric patterns with modern minimalism',
            'additional': 'Right-to-left design consideration with Islamic geometric influence'
        },
        'fr': {
            'name': 'CyclesSommeil',
            'colors': ('#7C3AED', '#C4B5FD'),
            'style': 'elegant',
            'cultural': 'French sophisticated design with subtle luxury',
            'additional': 'Parisian elegance meets modern health technology'
        },
        'de': {
            'name': 'SchlafZyklen',
            'colors': ('#4B5563', '#9CA3AF'),
            'style': 'professional',
            'cultural': 'German precision and functional design (Bauhaus influence)',
            'additional': 'Form follows function with clear information hierarchy'
        }
    }
    
    # Initialize generator with API key from .env
    generator = IconGenerator()
    
    # Output directory
    output_dir = Path('./sleep_app_icons')
    output_dir.mkdir(exist_ok=True)
    
    print("🌙 SleepCycles Icon Generation with Rich Context")
    print("=" * 60)
    print(f"📱 App: Sleep tracking and analysis")
    print(f"🎯 Audience: {app_context['audience']}")
    print(f"✨ Elements: {', '.join(app_context['elements'])}")
    print("=" * 60)
    
    successful = []
    failed = []
    
    for locale, config in locale_configs.items():
        print(f"\n📍 Generating {locale}: {config['name']}")
        print(f"   🎨 Style: {config['style']} | Colors: {config['colors'][0]} → {config['colors'][1]}")
        print(f"   🌍 Cultural: {config['cultural']}")
        
        try:
            # Generate icon with full context
            image = generator.generate_icon(
                app_name=config['name'],
                colors=config['colors'],
                style=config['style'],
                model='dalle-3',  # Use DALL-E 3 for best quality
                app_description=app_context['description'],
                icon_elements=app_context['elements'],
                target_audience=app_context['audience'],
                locale=locale,
                cultural_style=config['cultural'],
                additional_prompt=config['additional']
            )
            
            if image:
                # Save with locale-specific name
                success = generator.save_icon_set(
                    image=image,
                    output_dir=output_dir,
                    name_prefix=f"SleepCycles-{locale}"
                )
                
                if success:
                    successful.append(locale)
                    print(f"   ✅ Success!")
                else:
                    failed.append(locale)
                    print(f"   ❌ Failed to save")
            else:
                failed.append(locale)
                print(f"   ❌ Failed to generate")
                
        except Exception as e:
            failed.append(locale)
            print(f"   ❌ Error: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 GENERATION SUMMARY")
    print(f"{'='*60}")
    
    if successful:
        print(f"\n✅ Successful ({len(successful)}/{len(locale_configs)}):")
        for locale in successful:
            print(f"   • {locale}: {locale_configs[locale]['name']} - {locale_configs[locale]['cultural']}")
    
    if failed:
        print(f"\n❌ Failed ({len(failed)}/{len(locale_configs)}):")
        for locale in failed:
            print(f"   • {locale}: {locale_configs[locale]['name']}")
    
    print(f"\n📁 Icons saved to: {output_dir.absolute()}")
    print("\n💡 Tip: Icons include rich cultural context for better localization!")


if __name__ == "__main__":
    # Ensure API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Please set OPENAI_API_KEY in your .env file")
        print("   Copy .env.example to .env and add your API key")
    else:
        generate_sleep_app_icons()