"""
Hailo Calibration Data Generator
===============================

This module creates calibration datasets for Hailo quantization processes. It processes
images from a source directory, validates them, and prepares them in the format required
for Hailo's neural network quantization workflow.

The script performs the following operations:
    1. Searches for image files in the specified directory
    2. Validates image integrity
    3. Resizes and crops images to target dimensions
    4. Saves processed images in the calibration directory

Example:
    Basic usage from command line::
    
        $ python hailo_calibration_data.py --data_dir /path/to/images --target_dir calib_data
        
    With custom parameters::
    
        $ python hailo_calibration_data.py --data_dir /path/to/images \\
            --target_dir my_calib --image_size 416 416 --num_images 512

Note:
    The script maintains aspect ratio during resizing and uses center cropping
    to achieve the target dimensions. Images that are too small or corrupted
    are automatically skipped.

Requirements:
    - PIL (Pillow)
    - tqdm
    - Standard library modules (os, argparse, random)

Author: PFG Electronics Training Team
Date: June 2025
"""

from PIL import Image
import os
import argparse
from tqdm import tqdm
import random


def parse_arguments():
    """
    Parse command line arguments for the Hailo calibration data generator.
    
    This function sets up the argument parser with all required and optional
    parameters for configuring the calibration data generation process.
    
    Returns:
        argparse.Namespace: Parsed command line arguments containing:
            - data_dir (str): Path to the source dataset directory
            - target_dir (str): Directory where processed images will be saved
            - image_size (list): Target dimensions for processed images [width, height]
            - num_images (int): Maximum number of calibration images to generate
            - image_extensions (list): List of valid image file extensions
            
    Example:
        >>> args = parse_arguments()
        >>> print(args.data_dir)
        '/path/to/dataset'
    """
    parser = argparse.ArgumentParser(description="Create the calibration data for the Hailo quantization")
    parser.add_argument("--data_dir", type=str, required=True, help="The dataset path")
    parser.add_argument("--target_dir", type=str, default="calib", help="The target directory to save processed images")
    parser.add_argument("--image_size", nargs='+', type=int, default=(640, 640), help="Input image size")
    parser.add_argument("--num_images", type=int, default=1024, help="Number of calibration images")
    parser.add_argument("--image_extensions", nargs='+', type=str, default=['.jpg', '.jpeg', '.png'],
                        help="Image file extensions to look for")
    return parser.parse_args()


def resize_and_crop(img, target_w, target_h):
    """
    Resize and crop image to target size while maintaining aspect ratio.
    
    This function performs intelligent resizing by first scaling the image to ensure
    at least one dimension matches the target, then center-cropping to achieve
    the exact target dimensions. The aspect ratio is preserved during resizing.
    
    Args:
        img (PIL.Image.Image): Input PIL Image object to be processed
        target_w (int): Target width in pixels
        target_h (int): Target height in pixels
        
    Returns:
        PIL.Image.Image: Processed image with exact target dimensions
        
    Raises:
        ValueError: If image has invalid dimensions (0 width or height)
        ValueError: If image is too small to resize properly
        ValueError: If calculated crop bounds are invalid
        
    Example:
        >>> from PIL import Image
        >>> img = Image.open('input.jpg')
        >>> resized_img = resize_and_crop(img, 640, 640)
        >>> print(resized_img.size)
        (640, 640)
        
    Note:
        The function uses LANCZOS resampling for high-quality resizing and
        performs center cropping to maintain the most important image content.
    """
    # Validate input image dimensions to ensure they are non-zero
    if img.width == 0 or img.height == 0:
        raise ValueError("Image has invalid dimensions (0 width or height)")

    # Calculate scaling ratio to ensure the image covers the target dimensions
    # Use max() to ensure at least one dimension will match or exceed the target
    ratio = max(target_w / img.width, target_h / img.height)
    new_width = int(img.width * ratio)
    new_height = int(img.height * ratio)

    # Verify that the scaled dimensions are sufficient for cropping
    if new_width < target_w or new_height < target_h:
        raise ValueError(f"Image too small to resize properly: {img.size}")

    # Resize the image using high-quality LANCZOS resampling
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calculate center crop coordinates to extract the target region
    left = max((img.width - target_w) // 2, 0)
    top = max((img.height - target_h) // 2, 0)
    right = left + target_w
    bottom = top + target_h

    # Validate crop bounds to prevent errors during cropping
    if right > img.width or bottom > img.height:
        raise ValueError(f"Invalid crop bounds: {(left, top, right, bottom)} for image size {img.size}")

    # Perform the center crop to achieve exact target dimensions
    return img.crop((left, top, right, bottom))


def find_image_files(directory, extensions):
    """
    Find all image files with specified extensions in directory and its subdirectories.
    
    This function recursively traverses the given directory and all its subdirectories
    to locate image files that match the specified file extensions. The search is
    case-insensitive for file extensions.
    
    Args:
        directory (str): Root directory path to search for images
        extensions (list): List of file extensions to search for (e.g., ['.jpg', '.png'])
        
    Returns:
        list: List of absolute file paths to all found image files
        
    Example:
        >>> extensions = ['.jpg', '.jpeg', '.png']
        >>> image_files = find_image_files('/dataset/images', extensions)
        >>> print(f"Found {len(image_files)} images")
        Found 1500 images
        
    Note:
        The function performs case-insensitive extension matching, so it will
        find files with extensions like '.JPG', '.PNG', '.jpeg', etc.
    """
    image_files = []
    # Recursively walk through directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if file extension matches any of the specified extensions (case-insensitive)
            if any(file.lower().endswith(ext.lower()) for ext in extensions):
                image_files.append(os.path.join(root, file))
    return image_files


def validate_images(image_paths):
    """
    Return only valid images (non-corrupt) from the provided list of image paths.
    
    This function validates each image by attempting to open and verify it using PIL.
    Corrupted or unreadable images are automatically filtered out with appropriate
    error messages displayed to the user.
    
    Args:
        image_paths (list): List of file paths to image files to validate
        
    Returns:
        list: List of file paths to valid, non-corrupted images
        
    Example:
        >>> all_images = ['/path/img1.jpg', '/path/corrupted.jpg', '/path/img3.png']
        >>> valid_images = validate_images(all_images)
        Validating images...
        Skipping invalid image /path/corrupted.jpg: cannot identify image file
        >>> print(f"Valid images: {len(valid_images)}")
        Valid images: 2
        
    Note:
        The validation process uses PIL's verify() method which checks image
        integrity without fully loading the image into memory, making it
        efficient for large datasets.
    """
    valid_image_paths = []
    print("Validating images...")
    # Iterate through all image paths with progress bar
    for path in tqdm(image_paths):
        try:
            # Attempt to open and verify image integrity
            with Image.open(path) as img:
                img.verify()  # Verify image without loading into memory
            valid_image_paths.append(path)
        except Exception as e:
            # Log and skip corrupted or unreadable images
            print(f"Skipping invalid image {path}: {e}")
    return valid_image_paths


def main():
    """
    Main execution function for the Hailo calibration data generator.
    
    This function orchestrates the entire calibration data generation process:
    1. Parses command line arguments
    2. Creates output directory
    3. Searches for and validates images
    4. Processes images to target specifications
    5. Saves processed images for Hailo quantization
    
    The function handles various error conditions gracefully and provides
    informative feedback to the user throughout the process.
    
    Raises:
        SystemExit: If no images are found or no valid images remain after validation
        
    Example:
        The main function is called when the script is executed directly::
        
            $ python hailo_calibration_data.py --data_dir /dataset --num_images 512
    """
    # Parse command line arguments for configuration
    args = parse_arguments()

    # Create target directory for processed calibration images
    target_dir_path = args.target_dir
    os.makedirs(target_dir_path, exist_ok=True)

    # Search for all image files in the specified directory
    print(f"Searching for images in {args.data_dir}...")
    all_image_paths = find_image_files(args.data_dir, args.image_extensions)

    # Early exit if no images found
    if not all_image_paths:
        print(f"No images found in {args.data_dir} with extensions {args.image_extensions}")
        return

    # Validate image integrity and filter out corrupted files
    valid_image_paths = validate_images(all_image_paths)

    # Early exit if no valid images remain
    if not valid_image_paths:
        print("No valid images found after verification.")
        return

    # Prepare dataset for processing
    print(f"Found {len(valid_image_paths)} valid images.")
    random.shuffle(valid_image_paths)  # Randomize selection for better representation
    images_list = valid_image_paths[:args.num_images]  # Limit to requested number

    # Warn if fewer images available than requested
    if len(images_list) < args.num_images:
        print(f"Warning: Only using {len(images_list)} images (less than requested {args.num_images})")

    # Process each image for Hailo calibration dataset
    print("Creating calibration data for Hailo export...")
    for idx, filepath in tqdm(enumerate(images_list)):
        try:
            print(f"Processing {filepath}")
            # Open and convert image to RGB format (required for JPEG output)
            with Image.open(filepath) as img:
                img = img.convert("RGB")

                # Skip images that are too small for meaningful processing
                if img.width < 10 or img.height < 10:
                    raise ValueError(f"Image too small: {img.size}")

                # Resize and crop image to target dimensions
                processed_img = resize_and_crop(img, args.image_size[0], args.image_size[1])
                
                # Save processed image with sequential naming
                output_filepath = os.path.join(target_dir_path, f"processed_{idx}.jpg")
                processed_img.save(output_filepath, format="JPEG")

        except Exception as e:
            # Log processing errors but continue with remaining images
            print(f"Error processing {filepath}: {e}")
            continue


# Script entry point - execute main function when run directly
if __name__ == "__main__":
    main()
