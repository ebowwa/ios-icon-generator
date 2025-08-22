# iOS Icon Generator

AI-powered iOS app icon generation with localization support, using OpenAI's DALL-E and GPT-Image models via `ai_proxy_core`.

## 🏗️ Architecture

Modular, composable architecture following Single Responsibility Principle:

```
src/
├── icon_generator.py         # Main orchestrator
├── ai_generator.py           # AI image generation (DALL-E, GPT-Image)
├── image_processor.py        # iOS icon processing (12 sizes + Contents.json)
├── prompt_builder.py         # Cultural prompt construction (25+ locales)
└── ios_localization_reader.py # iOS project file reader (.strings files)
```

## ✨ Features

- 🎨 **AI Models**: DALL-E 3, DALL-E 2, GPT-Image-1
- 🌍 **Localization**: Reads InfoPlist.strings and Localizable.strings
- 🎯 **Cultural Context**: Design aesthetics for 25+ locales
- 📱 **iOS Ready**: Generates all 12 required sizes + Contents.json
- 🔧 **Composable**: Use modules independently or together
- 🚀 **Batch Generation**: Generate icons for all locales at once

## 📦 Installation

```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- OpenAI API key
- ai_proxy_core 0.4.3

## 🚀 Usage

### Basic Usage

```python
from src import IconGenerator

generator = IconGenerator()
generator.generate_icon(
    app_name="MyApp",
    colors=('#FF6B6B', '#4ECDC4'),
    output_dir=Path('./output'),
    model='dalle-3'
)
```

### Generate from iOS Project

Automatically reads localization files and generates culturally appropriate icons:

```python
from src import IconGenerator
from pathlib import Path

generator = IconGenerator()
generator.generate_from_ios_project(
    ios_project_path=Path('/path/to/iOS/app'),
    output_dir=Path('./output'),
    model='dalle-3'
)
```

### Use Individual Modules

Each module can be used independently:

```python
from src import (
    AIIconGenerator,
    IOSIconProcessor, 
    PromptBuilder,
    IOSLocalizationReader
)

# Read iOS localization
reader = IOSLocalizationReader()
context = reader.get_app_context_from_project(ios_path, 'en')

# Build culturally-aware prompt
builder = PromptBuilder()
prompt = builder.build_prompt(
    app_name="MyApp",
    locale='ja',
    cultural_style='Japanese minimalist design'
)

# Generate AI image
ai_gen = AIIconGenerator()
image = ai_gen.generate(prompt, model='dalle-3')

# Process for iOS
processor = IOSIconProcessor()
processor.save_ios_iconset(image, output_dir)
```

## 🌍 Supported Locales

The generator includes cultural design context for:

- 🇺🇸 English (en)
- 🇯🇵 Japanese (ja)
- 🇨🇳 Chinese Simplified (zh-Hans)
- 🇹🇼 Chinese Traditional (zh-Hant)
- 🇰🇷 Korean (ko)
- 🇪🇸 Spanish (es)
- 🇲🇽 Spanish Mexico (es-MX)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇮🇹 Italian (it)
- 🇵🇹 Portuguese (pt-BR)
- 🇷🇺 Russian (ru)
- 🇸🇦 Arabic (ar)
- 🇮🇳 Hindi (hi)
- 🇹🇭 Thai (th)
- 🇻🇳 Vietnamese (vi)
- 🇮🇩 Indonesian (id)
- 🇹🇷 Turkish (tr)
- 🇳🇱 Dutch (nl)
- 🇵🇱 Polish (pl)
- 🇸🇪 Swedish (sv)
- 🇳🇴 Norwegian (no)
- 🇩🇰 Danish (da)
- 🇫🇮 Finnish (fi)
- 🇬🇷 Greek (el)
- 🇮🇱 Hebrew (he)

## 📱 iOS Icon Sizes Generated

- 20pt: @2x (40×40), @3x (60×60)
- 29pt: @2x (58×58), @3x (87×87)
- 40pt: @2x (80×80), @3x (120×120)
- 60pt: @2x (120×120), @3x (180×180)
- 76pt: @1x (76×76), @2x (152×152)
- 83.5pt: @2x (167×167)
- 1024pt: @1x (1024×1024) - App Store

## 🔧 Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key'
# or create .env file
echo "OPENAI_API_KEY=your-api-key" > .env
```

## 📝 Examples

### Batch Generation for Multiple Locales

```python
from src import IconGenerator

generator = IconGenerator()

locales = ['en', 'ja', 'zh-Hans', 'es-MX']
for locale in locales:
    generator.generate_icon(
        app_name="SleepCycles",
        locale=locale,
        output_dir=Path(f'./icons/{locale}')
    )
```

### Custom Style and Elements

```python
generator.generate_icon(
    app_name="MyApp",
    colors=('#1E3A8A', '#60A5FA'),
    style='minimalist',
    icon_elements=['moon', 'stars', 'clouds'],
    app_description='Sleep tracking app',
    target_audience='Health-conscious individuals',
    cultural_style='Silicon Valley tech aesthetic'
)
```

## 🧪 Testing

```bash
# Test with English locale
python test_en_locale.py

# Test replacing actual app icons
python test_replace_actual.py
```

## 📁 Project Structure

```
ios-icon-generator/
├── src/                    # Core modules
│   ├── __init__.py
│   ├── icon_generator.py
│   ├── ai_generator.py
│   ├── image_processor.py
│   ├── prompt_builder.py
│   └── ios_localization_reader.py
├── legacy/                 # Previous monolithic version
├── example_batch.py        # Batch generation example
├── test_*.py              # Test scripts
├── requirements.txt
├── README.md
└── .gitignore
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

MIT

## 🙏 Credits

Built with [ai_proxy_core](https://github.com/AI-Northstar-Tech/ai-proxy-core) for OpenAI API integration.