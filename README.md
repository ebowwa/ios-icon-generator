# iOS Icon Generator

Generate professional iOS app icons using AI image generation powered by OpenAI's DALL-E and GPT-Image models via `ai_proxy_core`.

## 🆕 Version 2 - Refactored Architecture

The project now includes a refactored version (`icon_generator_v2.py`) with:
- **Modular architecture** following Single Responsibility Principle
- **iOS localization support** - reads InfoPlist.strings and Localizable.strings
- **Automatic multi-locale generation** from iOS projects
- **Cultural design context** for 25+ locales
- **Separated concerns** with dedicated modules for AI, image processing, and prompts

## Features

- 🎨 AI-powered icon generation using DALL-E 3, DALL-E 2, or GPT-Image-1
- 📱 Generates all required iOS icon sizes automatically
- 🎯 Creates Xcode-ready `.appiconset` directories
- 🌈 Customizable gradients and design styles
- 🔧 Simple CLI interface and Python API

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- OpenAI API key
- ai_proxy_core 0.4.3+

## Usage

### Command Line

```bash
# Basic usage
python icon_generator.py "MyApp"

# Custom colors and style
python icon_generator.py "MyApp" --colors "#FF6B6B" "#4ECDC4" --style modern

# Use GPT-Image-1 model
python icon_generator.py "MyApp" --model gpt-image-1 --style minimalist

# Specify output directory
python icon_generator.py "MyApp" --output ./icons/

# Add additional prompt details
python icon_generator.py "MyApp" --additional "Include a moon symbol in the design"
```

### Python API

```python
from icon_generator import IconGenerator
from pathlib import Path

# Initialize with API key
generator = IconGenerator(api_key="your-openai-api-key")

# Generate an icon
image = generator.generate_icon(
    app_name="MyApp",
    colors=("#1E3A8A", "#60A5FA"),
    style="minimalist",
    model="dalle-3"
)

# Save as complete icon set
generator.save_icon_set(
    image=image,
    output_dir=Path("./output"),
    name_prefix="MyApp"
)
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## Available Options

### Models
- `dalle-3` (default) - Best quality, slower
- `dalle-2` - Faster, good quality  
- `gpt-image-1` - Newest model, experimental

### Styles
- `minimalist` (default)
- `modern`
- `playful`
- `professional`
- `elegant`

### Colors
Specify as hex colors for gradient background:
- `--colors "#top-color" "#bottom-color"`

## Output

The generator creates:
- Complete `.appiconset` directory with all iOS sizes
- `Contents.json` file for Xcode compatibility
- Preview PNG file

### Generated Icon Sizes
- 20x20 (@2x, @3x)
- 29x29 (@2x, @3x)  
- 40x40 (@2x, @3x)
- 60x60 (@2x, @3x)
- 76x76 (@1x, @2x)
- 83.5x83.5 (@2x)
- 1024x1024 (App Store)

## Examples

```bash
# Minimalist blue gradient
python icon_generator.py "SleepApp" --colors "#1E3A8A" "#60A5FA"

# Modern green gradient with moon theme
python icon_generator.py "SleepApp" --colors "#059669" "#34D399" --style modern --additional "crescent moon symbol"

# Professional app with GPT-Image-1
python icon_generator.py "BusinessApp" --model gpt-image-1 --style professional --colors "#374151" "#9CA3AF"
```

## Dependencies

- `ai_proxy_core` - OpenAI API integration
- `Pillow` - Image processing
- `python-dotenv` - Environment variable loading

## License

MIT License