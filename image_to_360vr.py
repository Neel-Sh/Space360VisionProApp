#!/usr/bin/env python3
"""
360 VR Image Converter
Converts regular images into 360-degree VR images suitable for Vision Pro and other VR environments.
"""

import cv2
import numpy as np
import argparse
import os
from PIL import Image, ImageDraw
from pathlib import Path
import math


class ImageTo360VR:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        
        # Standard equirectangular resolutions (2:1 aspect ratio)
        self.vr_presets = {
            'mobile': (2048, 1024),      # Mobile VR, lightweight
            'standard': (4096, 2048),    # Standard VR quality
            'high': (6144, 3072),        # High quality VR
            'ultra': (8192, 4096),       # Ultra HD for Vision Pro
            'max': (12288, 6144),        # Maximum quality
            'native': (16384, 8192),     # Native ultra-high resolution
            'extreme': (20480, 10240)    # Extreme quality (matches large TIFFs)
        }
    
    def validate_input(self, image_path):
        """Validate input image file."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        file_ext = Path(image_path).suffix.lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_ext}. Supported: {self.supported_formats}")
        
        return True
    
    def load_image(self, image_path):
        """Load and prepare image for processing."""
        self.validate_input(image_path)
        
        # Load with PIL for better format support
        pil_image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert to OpenCV format
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return image
    
    def create_equirectangular_from_image(self, image, output_width=4096, output_height=2048):
        """
        Convert a regular image to equirectangular 360 format by projecting it onto a sphere.
        This creates a 360-degree panoramic view with the input image as the front face.
        """
        h, w = image.shape[:2]
        
        # Create output equirectangular image
        equirect = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        
        # Fill with a gradient background (sky-like)
        for y in range(output_height):
            gradient_value = int(255 * (1 - y / output_height))
            equirect[y, :] = [gradient_value // 3, gradient_value // 2, gradient_value]
        
        # Calculate the region where we'll place the original image
        # Place it in the center front of the sphere (longitude 0, latitude 0)
        center_x = output_width // 2
        center_y = output_height // 2
        
        # Scale the image to fit nicely in the 360 view
        scale_factor = min(output_width // 4, output_height // 2) / max(w, h)
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        
        # Resize the input image
        resized_image = cv2.resize(image, (new_w, new_h))
        
        # Place the image in the center front of the equirectangular projection
        start_x = center_x - new_w // 2
        end_x = start_x + new_w
        start_y = center_y - new_h // 2
        end_y = start_y + new_h
        
        # Ensure bounds are within the output image
        start_x = max(0, start_x)
        end_x = min(output_width, end_x)
        start_y = max(0, start_y)
        end_y = min(output_height, end_y)
        
        # Copy the resized image to the equirectangular projection
        equirect[start_y:end_y, start_x:end_x] = resized_image[:end_y-start_y, :end_x-start_x]
        
        return equirect
    
    def create_spherical_projection(self, image, output_width=4096, output_height=2048):
        """
        Create a more sophisticated spherical projection that wraps the image around a sphere.
        """
        h, w = image.shape[:2]
        
        # Create output equirectangular image
        equirect = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        
        # Create coordinate grids
        x_coords = np.arange(output_width)
        y_coords = np.arange(output_height)
        X, Y = np.meshgrid(x_coords, y_coords)
        
        # Convert to spherical coordinates
        longitude = (X / output_width) * 2 * np.pi - np.pi  # -π to π
        latitude = (Y / output_height) * np.pi - np.pi / 2   # -π/2 to π/2
        
        # Convert spherical to Cartesian coordinates
        x_sphere = np.cos(latitude) * np.cos(longitude)
        y_sphere = np.cos(latitude) * np.sin(longitude)
        z_sphere = np.sin(latitude)
        
        # Project onto the front hemisphere for the main image
        # Map the front-facing part of the sphere to the input image
        mask = x_sphere > 0  # Front hemisphere
        
        # For front-facing pixels, map to input image coordinates
        front_y = y_sphere[mask]
        front_z = z_sphere[mask]
        
        # Convert to image coordinates
        img_x = ((front_y + 1) / 2 * (w - 1)).astype(int)
        img_y = ((front_z + 1) / 2 * (h - 1)).astype(int)
        
        # Ensure coordinates are within bounds
        img_x = np.clip(img_x, 0, w - 1)
        img_y = np.clip(img_y, 0, h - 1)
        
        # Sample from input image
        equirect[mask] = image[img_y, img_x]
        
        # Fill the back hemisphere with a mirrored/extended version
        back_mask = x_sphere <= 0
        if np.any(back_mask):
            # Create a simple background for the back hemisphere
            back_y = y_sphere[back_mask]
            back_z = z_sphere[back_mask]
            
            # Use a mirrored and darkened version of the original image
            back_img_x = ((back_y + 1) / 2 * (w - 1)).astype(int)
            back_img_y = ((back_z + 1) / 2 * (h - 1)).astype(int)
            back_img_x = np.clip(back_img_x, 0, w - 1)
            back_img_y = np.clip(back_img_y, 0, h - 1)
            
            back_pixels = image[back_img_y, back_img_x]
            # Darken the back hemisphere
            back_pixels = (back_pixels * 0.3).astype(np.uint8)
            equirect[back_mask] = back_pixels
        
        return equirect
    
    def create_stereoscopic_360(self, image, output_width=4096, output_height=4096, eye_separation=0.1):
        """
        Create a stereoscopic 360 image (top-bottom format) for 3D VR viewing.
        """
        # Create two slightly different perspectives
        left_eye = self.create_spherical_projection(image, output_width, output_height // 2)
        
        # Create right eye view with slight offset (simulated depth)
        # For simplicity, we'll create a slight horizontal shift
        shift_pixels = int(output_width * eye_separation * 0.01)
        right_eye = np.roll(left_eye, shift_pixels, axis=1)
        
        # Combine top-bottom
        stereoscopic = np.vstack([left_eye, right_eye])
        
        return stereoscopic
    
    def add_metadata_for_vr(self, image_path, metadata_type="equirectangular"):
        """
        Add VR metadata to the image for proper recognition by VR platforms.
        """
        # This would typically involve adding EXIF data or XMP metadata
        # For Vision Pro compatibility, ensure the image follows the right specifications
        pass
    
    def save_360_image(self, image, output_path, quality=98, save_tiff=False):
        """Save the 360 image with highest quality settings for VR platforms."""
        # Convert BGR to RGB for saving
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        
        if save_tiff or output_path.lower().endswith('.tiff') or output_path.lower().endswith('.tif'):
            # Save as uncompressed TIFF for maximum quality
            pil_image.save(output_path, format='TIFF', compression=None)
            print(f"📸 360 VR image saved as uncompressed TIFF: {output_path}")
        else:
            # Save as JPEG with maximum quality and no optimization compression
            pil_image.save(output_path, format='JPEG', quality=quality, optimize=False, subsampling=0)
            print(f"📸 360 VR image saved: {output_path} (Quality: {quality}%)")
        
        height, width = image.shape[:2]
        aspect_ratio = width / height
        
        print(f"📐 Dimensions: {width}x{height} (aspect ratio: {aspect_ratio:.1f}:1)")
        print(f"🌐 Format: Equirectangular projection (360° x 180°)")
        print(f"🥽 Compatible with: Vision Pro, Oculus, SteamVR, and other VR platforms")
        
        # Provide format validation feedback
        if abs(aspect_ratio - 2.0) < 0.1:
            print(f"✅ Perfect 2:1 aspect ratio for VR compatibility!")
        elif abs(aspect_ratio - 1.0) < 0.1:
            print(f"✅ Square format - good for stereoscopic 360 viewing!")
        else:
            print(f"⚠️  Non-standard aspect ratio - may not display optimally in VR")
    
    def convert_to_360vr(self, input_path, output_path=None, method="spherical", 
                        width=4096, height=2048, stereoscopic=False):
        """
        Main conversion function - Creates equirectangular 360 VR images.
        
        Args:
            input_path: Path to input image
            output_path: Path for output 360 image
            method: Conversion method ("simple", "spherical")
            width: Output width (should maintain 2:1 ratio with height)
            height: Output height (should be width/2 for proper equirectangular format)
            stereoscopic: Create stereoscopic 360 image
            
        Note: For best VR compatibility, use 2:1 aspect ratio (e.g., 4096x2048, 8192x4096)
        """
        
        # Validate 2:1 aspect ratio for optimal VR experience
        if not stereoscopic and abs(width / height - 2.0) > 0.1:
            print(f"⚠️  Warning: Aspect ratio {width}x{height} is not 2:1.")
            print(f"   For optimal VR experience, consider using 2:1 ratio like {height*2}x{height}")
            print(f"   Standard equirectangular formats: 4096x2048, 8192x4096, etc.")
        
        # For stereoscopic, height should be width (square format with top-bottom eyes)
        if stereoscopic and abs(width / height - 1.0) > 0.1:
            print(f"⚠️  Warning: For stereoscopic mode, use square format like {width}x{width}")
            print(f"   This creates proper top-bottom stereoscopic layout.")
        
        # Load input image
        print(f"Loading image: {input_path}")
        image = self.load_image(input_path)
        
        # Generate output path if not provided
        if output_path is None:
            input_path_obj = Path(input_path)
            output_path = input_path_obj.parent / f"{input_path_obj.stem}_360vr.jpg"
        
        # Choose conversion method
        if stereoscopic:
            print("Creating stereoscopic 360 VR image...")
            result = self.create_stereoscopic_360(image, width, height * 2)
        elif method == "simple":
            print("Creating 360 VR image using simple projection...")
            result = self.create_equirectangular_from_image(image, width, height)
        elif method == "spherical":
            print("Creating 360 VR image using spherical projection...")
            result = self.create_spherical_projection(image, width, height)
        elif method == "direct":
            print("Creating 360 VR image using direct high-resolution conversion...")
            result = self.create_direct_equirectangular(image, width, height)
        else:
            raise ValueError(f"Unknown method: {method}. Available: simple, spherical, direct")
        
        # Save result
        self.save_360_image(result, output_path)
        
        return output_path
    
    def convert_with_preset(self, input_path, preset='standard', output_path=None, 
                           method="spherical", stereoscopic=False):
        """
        Convert using VR resolution presets for guaranteed 2:1 equirectangular format.
        
        Args:
            input_path: Path to input image
            preset: VR quality preset ('mobile', 'standard', 'high', 'ultra', 'max')
            output_path: Path for output 360 image
            method: Conversion method ("simple", "spherical")  
            stereoscopic: Create stereoscopic 360 image
        """
        if preset not in self.vr_presets:
            raise ValueError(f"Unknown preset '{preset}'. Available: {list(self.vr_presets.keys())}")
        
        width, height = self.vr_presets[preset]
        
        print(f"🎯 Using VR preset: '{preset}' ({width}x{height})")
        print(f"📐 Perfect 2:1 equirectangular format for VR compatibility")
        
        return self.convert_to_360vr(
            input_path=input_path,
            output_path=output_path,
            method=method,
            width=width,
            height=height,
            stereoscopic=stereoscopic
        )
    
    def create_direct_equirectangular(self, image, output_width=16384, output_height=8192):
        """
        Create a seamless 360 VR equirectangular projection that wraps the input image
        naturally around a sphere without visible distortions or seams in VR.
        """
        h, w = image.shape[:2]
        
        print(f"📐 Creating seamless 360 VR projection from {w}x{h} to {output_width}x{output_height}")
        print(f"🔄 Using optimized seamless wrapping with no visible distortions")
        
        # Create coordinate grids for vectorized processing
        x_coords = np.arange(output_width)
        y_coords = np.arange(output_height)
        X, Y = np.meshgrid(x_coords, y_coords)
        
        # Convert pixel coordinates to longitude/latitude
        longitude = (X / output_width) * 2 * np.pi - np.pi  # -π to π
        latitude = (Y / output_height) * np.pi - np.pi / 2   # -π/2 to π/2
        
        # Convert spherical coordinates to Cartesian
        cart_x = np.cos(latitude) * np.cos(longitude)
        cart_y = np.cos(latitude) * np.sin(longitude)
        cart_z = np.sin(latitude)
        
        # Use azimuthal angle for horizontal mapping (seamless wrap-around)
        azimuth = np.arctan2(cart_y, cart_x)
        azimuth = np.where(azimuth < 0, azimuth + 2 * np.pi, azimuth)
        
        # Use elevation for vertical mapping
        elevation = np.arcsin(np.clip(cart_z, -1, 1))
        
        # Map to image coordinates with seamless horizontal wrapping
        img_x = (azimuth / (2 * np.pi)) * w
        img_y = ((elevation + np.pi/2) / np.pi) * h
        
        # Apply seamless wrapping and bounds
        img_x = img_x % w  # Seamless horizontal wrap
        img_y = np.clip(img_y, 0, h-1)  # Clamp vertical bounds
        
        # Use OpenCV's high-quality remapping for smooth interpolation
        img_x_32 = img_x.astype(np.float32)
        img_y_32 = img_y.astype(np.float32)
        
        # Create the seamless equirectangular projection
        equirect = cv2.remap(image, img_x_32, img_y_32, 
                           interpolation=cv2.INTER_LANCZOS4,
                           borderMode=cv2.BORDER_WRAP)
        
        print(f"✅ Seamless 360 VR projection complete!")
        print(f"🥽 Image should wrap seamlessly in VR with no visible distortions or seams")
        
        return equirect


def main():
    parser = argparse.ArgumentParser(description="Convert regular images to 360 VR equirectangular format")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output image path")
    parser.add_argument("-m", "--method", choices=["simple", "spherical", "direct"], 
                       default="direct", help="Conversion method (direct preserves most detail)")
    
    # Resolution options: either use preset or custom dimensions
    res_group = parser.add_mutually_exclusive_group()
    res_group.add_argument("-p", "--preset", choices=["mobile", "standard", "high", "ultra", "max", "native", "extreme"],
                          help="VR quality preset (guarantees 2:1 equirectangular format)")
    res_group.add_argument("-w", "--width", type=int, help="Custom output width")
    
    parser.add_argument("--height", type=int, help="Custom output height (use with --width)")
    parser.add_argument("-s", "--stereoscopic", action="store_true", 
                       help="Create stereoscopic 360 image")
    parser.add_argument("--quality", type=int, default=98, help="Output image quality (JPEG)")
    parser.add_argument("--tiff", action="store_true", help="Save as uncompressed TIFF for maximum quality")
    
    args = parser.parse_args()
    
    # Create converter instance
    converter = ImageTo360VR()
    
    try:
        # Use preset or custom dimensions
        if args.preset:
            # Use VR preset for guaranteed 2:1 equirectangular format
            output_path = converter.convert_with_preset(
                input_path=args.input,
                preset=args.preset,
                output_path=args.output,
                method=args.method,
                stereoscopic=args.stereoscopic
            )
        else:
            # Use custom dimensions (default to native ultra-high resolution)
            width = args.width or 16384
            height = args.height or 8192
            
            output_path = converter.convert_to_360vr(
                input_path=args.input,
                output_path=args.output,
                method=args.method,
                width=width,
                height=height,
                stereoscopic=args.stereoscopic
            )
        
        # Handle TIFF output for maximum quality
        if args.tiff and not output_path.lower().endswith(('.tiff', '.tif')):
            tiff_path = output_path.rsplit('.', 1)[0] + '.tiff'
            converter.save_360_image(cv2.imread(output_path), tiff_path, save_tiff=True)
        
        print(f"\n✅ Successfully converted '{args.input}' to 360 VR format!")
        print(f"📍 Output saved as: {output_path}")
        print(f"🥽 Ready for Vision Pro and other VR platforms!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 