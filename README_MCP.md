# iOS Icon Generator - Claude Code MCP Integration

This project now includes a Model Context Protocol (MCP) server that integrates with Claude Code, allowing you to generate iOS icons directly through Claude.

## Features

- **AI-Powered Icon Generation**: Generate iOS app icons using DALL-E 2/3
- **Localization Support**: Automatically detect and generate icons for all iOS localizations
- **Cultural Design Adaptation**: Locale-specific design aesthetics
- **Full Icon Set Generation**: All required iOS icon sizes with proper Contents.json
- **Claude Code Integration**: Use directly within Claude Code conversations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

### 3. Run MCP Server

```bash
./run_mcp.sh
```

Or manually:
```bash
python mcp_server.py --host localhost --port 3000
```

## Available MCP Tools

### 1. `generate_icon`
Generate a single iOS app icon with customization options.

**Parameters:**
- `app_name` (required): Name of the app
- `colors`: Gradient colors [top, bottom] in hex format
- `style`: Design style (minimalist, modern, etc.)
- `model`: AI model (dalle-3, dalle-2, gpt-image-1)
- `app_description`: Description of the app
- `icon_elements`: Visual elements to include
- `target_audience`: Target audience
- `locale`: Language/region code
- `cultural_style`: Cultural design preferences
- `output_dir`: Where to save the icons

### 2. `generate_from_project`
Generate icons for all localizations in an iOS project.

**Parameters:**
- `ios_project_path` (required): Path to iOS project
- `colors`: Gradient colors
- `style`: Design style
- `model`: AI model to use
- `output_dir`: Output directory

### 3. `get_localizations`
Get all available localizations from an iOS project.

**Parameters:**
- `ios_project_path` (required): Path to iOS project

### 4. `list_cultural_styles`
List available cultural design styles for different locales.

## Usage in Claude Code

Once the MCP server is running, you can use it in Claude Code conversations:

```
Claude, please generate an iOS icon for my "Weather Tracker" app with blue gradient colors and minimalist style.

Claude, generate icons for all localizations in my iOS project at /path/to/project

Claude, what localizations are available in my iOS project?
```

## Configuration

### Claude Code Configuration

Add to your Claude Code settings (claude_mcp_config.json):

```json
{
  "mcpServers": {
    "ios-icon-generator": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  }
}
```

## Supported Locales & Cultural Styles

The system includes cultural design contexts for 25+ locales including:
- English (US, GB)
- Japanese (wa aesthetic)
- Korean (K-design)
- Chinese (Simplified/Traditional)
- Spanish (ES, MX)
- French
- German (Bauhaus influence)
- Italian
- Portuguese (BR)
- Arabic (RTL support)
- Scandinavian languages
- And more...

## Output Structure

Generated icons are saved in the following structure:
```
output_dir/
├── AppIcon-en.appiconset/
│   ├── AppIcon-20@2x.png
│   ├── AppIcon-20@3x.png
│   ├── ... (all iOS sizes)
│   └── Contents.json
├── AppIcon-en_preview.png
├── AppIcon-ja.appiconset/
│   └── ... (same structure)
└── AppIcon-ja_preview.png
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Direct Python Usage
```python
from src.icon_generator import IconGenerator

generator = IconGenerator(api_key="your-key")
generator.generate_icon(
    app_name="My App",
    colors=("#1E3A8A", "#60A5FA"),
    output_dir=Path("./icons")
)
```

## Troubleshooting

### MCP Server Won't Start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed
- Verify OPENAI_API_KEY is set

### Icon Generation Fails
- Check OpenAI API key validity
- Ensure sufficient API credits
- Verify network connectivity

### Localization Not Detected
- Check .lproj directories exist in iOS project
- Verify InfoPlist.strings or Localizable.strings files present

## License

MIT License - See LICENSE file for details