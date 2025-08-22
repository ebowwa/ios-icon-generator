#!/usr/bin/env python3
"""
Example batch generation script for multiple localized icons
"""

from icon_generator import IconGenerator
from pathlib import Path


def generate_localized_icons():
    """Generate icons for multiple locales"""
    
    # Configuration for different locales
    locale_configs = {
        'en': {
            'name': 'SleepLoops',
            'colors': ('#1E3A8A', '#60A5FA'),
            'style': 'minimalist',
            'additional': 'Clean, modern design with crescent moon'
        },
        'es': {
            'name': 'CiclosSueño',
            'colors': ('#EA580C', '#FB923C'),
            'style': 'modern',
            'additional': 'Warm orange gradient with moon symbol'
        },
        'fr': {
            'name': 'CyclesSommeil',
            'colors': ('#7C3AED', '#C4B5FD'),
            'style': 'elegant',
            'additional': 'Purple gradient with elegant moon'
        },
        'de': {
            'name': 'SchlafZyklen',
            'colors': ('#4B5563', '#9CA3AF'),
            'style': 'professional',
            'additional': 'Professional gray gradient'
        },
        'ja': {
            'name': 'SleepApp',  # Using English name for better AI generation
            'colors': ('#1F2937', '#F59E0B'),
            'style': 'minimalist',
            'additional': 'Dark to amber gradient, zen style'
        }
    }
    
    # Initialize generator
    generator = IconGenerator()
    
    # Output directory
    output_dir = Path('./generated_icons')
    output_dir.mkdir(exist_ok=True)
    
    successful = []
    failed = []
    
    print("🚀 Generating Localized Icons")
    print("=" * 50)
    
    for locale, config in locale_configs.items():
        print(f"\n📱 Generating {locale}: {config['name']}")
        
        try:
            # Generate icon
            image = generator.generate_icon(
                app_name=config['name'],
                colors=config['colors'],
                style=config['style'],
                model='dalle-3',
                additional_prompt=config['additional']
            )
            
            if image:
                # Save icon set
                success = generator.save_icon_set(
                    image=image,
                    output_dir=output_dir,
                    name_prefix=f"AppIcon-{locale}"
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
    print(f"\n{'='*50}")
    print("📊 GENERATION SUMMARY")
    print(f"{'='*50}")
    
    if successful:
        print(f"\n✅ Successful ({len(successful)}):")
        for locale in successful:
            print(f"   • {locale}: {locale_configs[locale]['name']}")
    
    if failed:
        print(f"\n❌ Failed ({len(failed)}):")
        for locale in failed:
            print(f"   • {locale}: {locale_configs[locale]['name']}")
    
    print(f"\n📁 Icons saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    generate_localized_icons()