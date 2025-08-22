#!/usr/bin/env python3
"""
Test that replaces the actual English icons in the SleepCycles app
"""

from pathlib import Path
from src import IconGenerator, IOSLocalizationReader
import shutil
from datetime import datetime

def test_replace_actual_icons():
    """Replace the actual English icons in SleepCycles"""
    
    # Paths
    ios_resources_path = Path('/Users/ebowwa/apps/ios/sleepApp/v2/SleepCycles/Products/SleepCycles/Resources')
    actual_icon_path = Path('/Users/ebowwa/apps/ios/sleepApp/v2/SleepCycles/Products/SleepCycles/Resources/Assets.xcassets/AppIcons/AppIcon-en.appiconset')
    
    print("🎯 TEST: Replacing actual English icons in SleepCycles")
    print("=" * 60)
    print(f"Target: {actual_icon_path}")
    
    # First, backup the current icons
    backup_path = actual_icon_path.parent / f"AppIcon-en.appiconset.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if actual_icon_path.exists():
        print(f"📦 Creating backup: {backup_path.name}")
        shutil.copytree(actual_icon_path, backup_path)
    
    # Read localization context
    print("\n📖 Reading iOS localization context...")
    context = IOSLocalizationReader.get_app_context_from_project(ios_resources_path, 'en')
    
    print(f"  • App Name: {context.get('display_name', 'SleepCycles')}")
    print(f"  • Found {len(context.get('localized_strings', {}))} localized strings")
    
    # Key strings from localization
    app_display_name = context.get('display_name', 'SleepCycles')
    
    # From Localizable.strings we know:
    # "app.name" = "SleepLoops"
    # "app.tagline" = "Better Sleep, Better Life"
    
    print("\n🎨 Generating new icon with localization context...")
    print("  • Using app name from localization")
    print("  • Applying Silicon Valley tech aesthetic")
    print("  • Including moon, stars, and clouds elements")
    
    try:
        # Initialize generator
        generator = IconGenerator()
        
        # Generate directly to the actual location
        # We'll use the parent directory and let it create AppIcon-en.appiconset
        output_dir = actual_icon_path.parent
        
        # Generate icon for English locale
        success = generator.generate_icon(
            app_name="SleepLoops",  # Using the actual localized app name
            colors=('#1E3A8A', '#60A5FA'),  # Blue gradient as specified
            output_dir=output_dir,
            style='minimalist',
            model='dalle-3',
            app_description='Sleep tracking app that helps you wake up refreshed by calculating optimal sleep cycles. Better Sleep, Better Life.',
            icon_elements=['crescent moon', 'stars', 'soft clouds', 'sleep cycles visualization'],
            target_audience='Health-conscious individuals who want to optimize their sleep patterns',
            locale='en',
            cultural_style='Clean Silicon Valley tech aesthetic with calming sleep theme',
            ios_project_path=ios_resources_path,
            additional_prompt='Modern, calming design. The gradient should be deep blue to light blue. Include subtle sleep cycle waves. Professional App Store quality.'
        )
        
        if success:
            print("\n✅ SUCCESS: Icon generated and saved!")
            print(f"📁 Location: {actual_icon_path}")
            
            # List the files that were created
            if actual_icon_path.exists():
                files = list(actual_icon_path.glob("*.png"))
                print(f"\n📱 Generated {len(files)} icon files:")
                for f in sorted(files)[:5]:  # Show first 5
                    print(f"   • {f.name}")
                print(f"   ... and {len(files) - 5} more") if len(files) > 5 else None
                
                # Check Contents.json
                contents_json = actual_icon_path / "Contents.json"
                if contents_json.exists():
                    print("   ✓ Contents.json created")
            
            print("\n🎯 TEST PASSED: Actual icons have been replaced!")
            print(f"💾 Backup saved as: {backup_path.name}")
            
        else:
            print("\n❌ FAILED: Could not generate icon")
            # Restore backup if it failed
            if backup_path.exists():
                print("🔄 Restoring backup...")
                shutil.rmtree(actual_icon_path, ignore_errors=True)
                shutil.copytree(backup_path, actual_icon_path)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Restore backup on error
        if backup_path.exists():
            print("🔄 Restoring backup due to error...")
            shutil.rmtree(actual_icon_path, ignore_errors=True)
            shutil.copytree(backup_path, actual_icon_path)

if __name__ == "__main__":
    test_replace_actual_icons()