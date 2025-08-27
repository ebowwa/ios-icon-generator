#!/usr/bin/env python3
"""
iOS Localization Reader
Reads InfoPlist.strings and Localizable.strings files for context
"""

import re
import plistlib
from pathlib import Path
from typing import Dict, List, Any


class IOSLocalizationReader:
    """Read iOS localization files for app context"""
    @staticmethod
    def read_strings_file(file_path: Path) -> Dict[str, str]:
        """
        Read a .strings file and return key-value pairs
        
        Args:
            file_path: Path to .strings file
            
        Returns:
            Dictionary of localization keys and values
        """
        strings = {}
        if not file_path.exists():
            return strings
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Pattern to match "key" = "value"; format
            pattern = r'"([^"]+)"\s*=\s*"([^"]+)"\s*;'
            matches = re.findall(pattern, content)
            for key, value in matches:
                strings[key] = value
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
        return strings

    @staticmethod
    def read_infoplist(file_path: Path) -> Dict:
        """
        Read Info.plist file
        
        Args:
            file_path: Path to Info.plist file
            
        Returns:
            Dictionary of plist contents
        """
        try:
            with open(file_path, 'rb') as f:
                plist = plistlib.load(f)
            return plist
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return {}

    @staticmethod
    def get_app_context_from_project(project_path: Path, locale: str = "en") -> Dict[str, Any]:
        """
        Extract app context from iOS project files
        
        Args:
            project_path: Path to iOS project root
            locale: Language code (e.g., 'en', 'ja', 'es')
            
        Returns:
            Dictionary with app context including name, description, etc.
        """
        context = {
            'app_name': '',
            'display_name': '',
            'description': '',
            'keywords': [],
            'category': '',
            'localized_strings': {}
        }
        # Common paths for iOS projects
        lproj_dir = project_path / f"{locale}.lproj"
        base_lproj = project_path / "Base.lproj"
        # Try to find InfoPlist.strings
        infoplist_paths = [
            lproj_dir / "InfoPlist.strings",
            base_lproj / "InfoPlist.strings",
            project_path / "InfoPlist.strings"
        ]
        for path in infoplist_paths:
            if path.exists():
                strings = IOSLocalizationReader.read_strings_file(path)
                context['app_name'] = strings.get('CFBundleName', '')
                context['display_name'] = strings.get('CFBundleDisplayName', '')
                break
        # Try to find Localizable.strings
        localizable_paths = [
            lproj_dir / "Localizable.strings",
            base_lproj / "Localizable.strings",
            project_path / "Localizable.strings"
        ]
        for path in localizable_paths:
            if path.exists():
                context['localized_strings'] = IOSLocalizationReader.read_strings_file(path)
                break
        # Try to find Info.plist
        info_plist_paths = [
            project_path / "Info.plist",
            project_path / "Resources" / "Info.plist",
            project_path / "Supporting Files" / "Info.plist"
        ]
        for path in info_plist_paths:
            if path.exists():
                plist = IOSLocalizationReader.read_infoplist(path)
                if not context['app_name']:
                    context['app_name'] = plist.get('CFBundleName', '')
                if not context['display_name']:
                    context['display_name'] = plist.get('CFBundleDisplayName', '')
                context['category'] = plist.get('LSApplicationCategoryType', '')
                break
        return context

    @staticmethod
    def find_all_localizations(project_path: Path) -> List[str]:
        """
        Find all available localizations in project
        
        Args:
            project_path: Path to iOS project root
            
        Returns:
            List of locale codes found
        """
        locales = []
        # Look for .lproj directories
        for item in project_path.iterdir():
            if item.is_dir() and item.name.endswith('.lproj'):
                locale = item.name.replace('.lproj', '')
                if locale != 'Base':
                    locales.append(locale)
        return locales
