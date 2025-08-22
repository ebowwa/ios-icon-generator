#!/usr/bin/env python3
"""
Test the icon generator with English localization from SleepCycles
"""

from pathlib import Path
from src import IconGenerator, IOSLocalizationReader

def test_english_locale():
    """Test with the English locale from SleepCycles"""
    
    # Path to the iOS project resources
    ios_resources_path = Path('/Users/ebowwa/apps/ios/sleepApp/v2/SleepCycles/Products/SleepCycles/Resources')
    
    # First, let's read what we can find
    print("📖 Reading iOS localization...")
    print("=" * 60)
    
    # Get context for English
    context = IOSLocalizationReader.get_app_context_from_project(ios_resources_path, 'en')
    
    print(f"App Name: {context.get('app_name', 'Not found')}")
    print(f"Display Name: {context.get('display_name', 'Not found')}")
    print(f"Description: {context.get('description', 'Not found')}")
    print(f"Category: {context.get('category', 'Not found')}")
    
    if context.get('localized_strings'):
        print(f"\nLocalized strings found: {len(context['localized_strings'])} entries")
        for key, value in list(context['localized_strings'].items())[:3]:
            print(f"  • {key}: {value[:50]}...")
    
    print("\n" + "=" * 60)
    print("🎨 Generating icon with this context...")
    
    try:
        # Initialize generator
        generator = IconGenerator()
        
        # Generate icon for English locale
        success = generator.generate_icon(
            app_name=context.get('display_name', 'SleepCycles'),
            colors=('#1E3A8A', '#60A5FA'),  # Blue gradient
            output_dir=Path('./test_output'),
            style='minimalist',
            model='dalle-3',
            app_description='Sleep tracking app that analyzes sleep patterns and provides insights',
            icon_elements=['crescent moon', 'stars', 'soft clouds'],
            target_audience='People who want to improve their sleep quality',
            locale='en',
            cultural_style='Clean Silicon Valley tech aesthetic',
            ios_project_path=ios_resources_path,
            additional_prompt='Modern, calming design that suggests rest and technology'
        )
        
        if success:
            print("✅ Icon generated successfully!")
            print("📁 Check ./test_output/AppIcon.appiconset/")
        else:
            print("❌ Failed to generate icon")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_english_locale()