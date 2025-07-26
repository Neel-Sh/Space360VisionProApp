#!/usr/bin/env python3
"""
Example usage of the ImageTo360VR converter
This script demonstrates how to use the converter programmatically.
"""

from image_to_360vr import ImageTo360VR
import os
from pathlib import Path


def example_conversions():
    """Run example conversions with different methods."""
    
    # Initialize the converter
    converter = ImageTo360VR()
    
    # Use the specific vr.tiff file
    input_image = "vr.tiff"  # Hard-coded to use your vr.tiff file
    
    if not os.path.exists(input_image):
        print(f"❌ vr.tiff not found in current directory")
        print("Please ensure vr.tiff is in the same folder as this script")
        return
    
    print("🔄 Starting 360 VR conversion of vr.tiff...")
    
    try:
        # Example 1: Basic spherical conversion
        print("\n1️⃣ Creating basic 360 VR image with spherical projection...")
        output1 = converter.convert_to_360vr(
            input_path=input_image,
            output_path="output_spherical_360.jpg",
            method="spherical",
            width=4096,
            height=2048
        )
        
        # Example 2: Simple equirectangular conversion
        print("\n2️⃣ Creating simple 360 VR image...")
        output2 = converter.convert_to_360vr(
            input_path=input_image,
            output_path="output_simple_360.jpg",
            method="simple",
            width=4096,
            height=2048
        )
        
        # Example 3: Stereoscopic 360 for 3D VR
        print("\n3️⃣ Creating stereoscopic 360 VR image for 3D viewing...")
        output3 = converter.convert_to_360vr(
            input_path=input_image,
            output_path="output_stereoscopic_360.jpg",
            method="spherical",
            width=4096,
            height=2048,
            stereoscopic=True
        )
        
        # Example 4: Using VR preset for guaranteed 2:1 equirectangular format
        print("\n4️⃣ Using 'ultra' preset for Vision Pro (guaranteed 2:1 format)...")
        output4 = converter.convert_with_preset(
            input_path=input_image,
            preset="ultra",  # 8192x4096 resolution
            output_path="output_visionpro_360.jpg",
            method="spherical"
        )
        
        # Example 5: Mobile VR preset
        print("\n5️⃣ Creating mobile VR version with 'mobile' preset...")
        output5 = converter.convert_with_preset(
            input_path=input_image,
            preset="mobile",  # 2048x1024 resolution
            output_path="output_mobile_360.jpg",
            method="spherical"
        )
        
        print("\n✅ All conversions completed successfully!")
        print("\n📁 Generated files:")
        for output in [output1, output2, output3, output4, output5]:
            if os.path.exists(output):
                size = os.path.getsize(output) / (1024*1024)
                print(f"   • {output} ({size:.1f} MB)")
        
        print("\n🥽 These images are ready for use in:")
        print("   • Vision Pro environments")
        print("   • Oculus/Meta Quest")
        print("   • SteamVR")
        print("   • Any VR platform supporting equirectangular 360 images")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")


def create_sample_image():
    """Create a simple sample image for testing if none exists."""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a colorful sample image
    img = Image.new('RGB', (800, 600), color='skyblue')
    draw = ImageDraw.Draw(img)
    
    # Add some visual elements
    draw.rectangle([100, 100, 700, 500], fill='lightgreen', outline='darkgreen', width=3)
    draw.ellipse([200, 150, 600, 450], fill='yellow', outline='orange', width=3)
    draw.text((300, 250), "Sample Image", fill='black')
    draw.text((250, 300), "for 360 VR Conversion", fill='black')
    
    img.save("sample_image.jpg", quality=95)
    print("📸 Created sample_image.jpg for testing")


if __name__ == "__main__":
    print("🌟 360 VR Image Converter - VR.TIFF Processing")
    print("=" * 50)
    
    # Run the examples with vr.tiff
    example_conversions() 