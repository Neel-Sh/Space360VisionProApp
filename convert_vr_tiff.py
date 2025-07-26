#!/usr/bin/env python3
"""
VR.TIFF to 360 VR Converter
Specifically designed to convert the vr.tiff file to various 360 VR formats.
"""

from image_to_360vr import ImageTo360VR
import os


def convert_vr_tiff():
    """Convert the specific vr.tiff file to Vision Pro optimized 360 VR format."""
    
    # Hard-coded input file
    input_file = "deepspace.tiff"
    
    # Verify the file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found in current directory")
        return False
    
    print("🥽 Converting vr.tiff to Vision Pro 360 VR format")
    print("=" * 50)
    
    # Initialize converter
    converter = ImageTo360VR()
    
    try:
        # Vision Pro Ultra Quality (8K) - Seamless projection
        print("\n🥽 Creating Vision Pro version (8192x4096) - SEAMLESS...")
        vision_pro_output = converter.convert_with_preset(
            input_path=input_file,
            preset="ultra",
            output_path="vr_360_visionpro.jpg",
            method="direct"  # Use seamless direct method
        )
        
        print("\n" + "=" * 50)
        print("✅ Vision Pro conversion completed successfully!")
        
        # Show file details
        if os.path.exists(vision_pro_output):
            size_mb = os.path.getsize(vision_pro_output) / (1024*1024)
            print(f"\n📁 Generated Vision Pro 360 VR file:")
            print(f"   • Vision Pro: {vision_pro_output} ({size_mb:.1f} MB)")
        
        print("\n🎯 Perfect equirectangular format (2:1 aspect ratio)")
        print("🥽 Optimized for Apple Vision Pro!")
        print("🔄 Seamless projection with no visible distortions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False


def quick_convert():
    """Quick single conversion optimized for Vision Pro."""
    
    input_file = "vr.tiff"
    
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found")
        return
    
    print("🚀 Quick Vision Pro conversion of vr.tiff...")
    
    converter = ImageTo360VR()
    
    output = converter.convert_with_preset(
        input_path=input_file,
        preset="ultra",  # 8192x4096 - perfect for Vision Pro
        output_path="vr_360_quick.jpg",
        method="spherical"
    )
    
    print(f"\n✅ Quick conversion complete: {output}")
    size_mb = os.path.getsize(output) / (1024*1024)
    print(f"📏 File size: {size_mb:.1f} MB")
    print(f"🥽 Ready for Vision Pro!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        # Quick conversion mode
        quick_convert()
    else:
        # Full conversion suite
        convert_vr_tiff() 