# 360 VR Image Converter 🥽

Convert regular images into 360-degree VR images suitable for Vision Pro and other VR environments.

## Features

✨ **Perfect Equirectangular Format**
- **2:1 Aspect Ratio** - Standard 4096x2048, 8192x4096, etc.
- **Guaranteed VR Compatibility** - Works perfectly in all VR platforms
- **Built-in Format Validation** - Warns if aspect ratio isn't optimal

🎯 **VR Platform Support**
- Apple Vision Pro
- Meta Quest / Oculus
- SteamVR
- Any platform supporting equirectangular 360 images

📐 **Smart Resolution Presets**
- **Mobile**: 2048x1024 (lightweight)
- **Standard**: 4096x2048 (default quality)  
- **High**: 6144x3072 (enhanced quality)
- **Ultra**: 8192x4096 (Vision Pro optimized)
- **Max**: 12288x6144 (maximum quality)

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line Usage

Convert any image to 360 VR format:

```bash
# Basic conversion (uses standard 4096x2048 equirectangular)
python image_to_360vr.py your_image.jpg

# Use VR preset for guaranteed 2:1 format
python image_to_360vr.py input.jpg -p ultra    # 8192x4096 for Vision Pro
python image_to_360vr.py input.jpg -p standard # 4096x2048 default
python image_to_360vr.py input.jpg -p mobile   # 2048x1024 lightweight

# Custom dimensions (will warn if not 2:1 ratio)
python image_to_360vr.py input.jpg -w 4096 --height 2048

# Create stereoscopic 360 image
python image_to_360vr.py input.jpg -s
```

### Programmatic Usage

```python
from image_to_360vr import ImageTo360VR

# Initialize converter
converter = ImageTo360VR()

# Method 1: Use VR preset (recommended - guarantees 2:1 format)
output_path = converter.convert_with_preset(
    input_path="my_image.jpg",
    preset="ultra",  # Perfect for Vision Pro
    output_path="my_360_image.jpg"
)

# Method 2: Custom dimensions 
output_path = converter.convert_to_360vr(
    input_path="my_image.jpg",
    width=4096, height=2048,  # 2:1 ratio
    method="spherical"
)
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Input image path | Required |
| `-o, --output` | Output image path | Auto-generated |
| `-m, --method` | Conversion method (`simple`, `spherical`) | `spherical` |
| `-p, --preset` | VR preset (`mobile`, `standard`, `high`, `ultra`, `max`) | - |
| `-w, --width` | Custom output width | `4096` |
| `--height` | Custom output height | `2048` |
| `-s, --stereoscopic` | Create stereoscopic 360 image | `false` |
| `--quality` | Output image quality (1-100) | `95` |

**Note:** Use `-p` for guaranteed 2:1 equirectangular format, or `-w` and `--height` for custom dimensions.

## Conversion Methods

### Spherical Projection (Recommended)
- Creates realistic spherical mapping
- Input image appears on front hemisphere
- Back hemisphere filled with darkened version
- Best for immersive VR experiences

### Simple Projection
- Places image in center of 360 canvas
- Surrounds with gradient background
- Faster processing
- Good for quick previews

### Stereoscopic Mode
- Creates top-bottom stereoscopic format
- Provides 3D depth perception
- Double the height (e.g., 4096x4096)
- Compatible with 3D VR viewers

## Recommended Settings

### For Vision Pro (Ultra Quality)
```bash
python image_to_360vr.py input.jpg -p ultra    # 8192x4096 equirectangular
```

### For Meta Quest/Oculus (Standard Quality) 
```bash
python image_to_360vr.py input.jpg -p standard # 4096x2048 equirectangular
```

### For Mobile VR (Lightweight)
```bash
python image_to_360vr.py input.jpg -p mobile   # 2048x1024 equirectangular
```

### For 3D Stereoscopic VR
```bash
python image_to_360vr.py input.jpg -p standard -s  # Creates 4096x4096 top-bottom
```

## Examples

Run the example script to see different conversion methods:

```bash
python example_usage.py
```

This will create:
- Basic spherical 360 image
- Simple projection 360 image  
- Stereoscopic 360 image
- High-resolution Vision Pro version

## Supported Formats

**Input:** JPG, JPEG, PNG, BMP, TIFF, WebP  
**Output:** JPG (high quality, optimized for VR)

## How It Works

1. **Load Input Image**: Validates and loads your image
2. **Spherical Mapping**: Projects image onto a virtual sphere
3. **Equirectangular Conversion**: Converts sphere to 360 format
4. **VR Optimization**: Saves with optimal settings for VR platforms

## Technical Details

- **Projection**: Equirectangular (360° x 180°)
- **Aspect Ratio**: 2:1 (standard for VR)
- **Color Space**: RGB
- **Coordinate System**: Longitude (-π to π), Latitude (-π/2 to π/2)

## Tips for Best Results

🎨 **Image Selection**
- Use high-resolution source images
- Images with clear subjects work best
- Avoid heavily distorted images

🔧 **Settings**
- Use `spherical` method for realistic results
- Higher resolution for better VR quality
- Enable stereoscopic for 3D effect

🥽 **VR Viewing**
- Images appear with source in front view
- Look around to see the full 360 environment
- Works in any VR app supporting equirectangular images

## Troubleshooting

**"Image file not found"**
- Check file path is correct
- Ensure file exists and is readable

**"Unsupported format"**
- Convert image to JPG, PNG, or other supported format

**Poor quality output**
- Increase output resolution with `--width` and `--height`
- Use higher quality source image

## Requirements

- Python 3.7+
- OpenCV
- Pillow (PIL)
- NumPy

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Found a bug or want to add features? Contributions welcome!

---

**Ready to create immersive VR experiences? Start converting your images today! 🚀** 