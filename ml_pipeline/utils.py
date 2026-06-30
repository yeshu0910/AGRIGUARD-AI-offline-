"""
Utility functions for AgriGuard AI crop disease detection system.

This module provides common utility functions for logging, file operations,
image processing, and other shared functionality.
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

import numpy as np
from PIL import Image


def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: Logging level (default: logging.INFO)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('agriguard.log')
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def save_json(data: Dict[str, Any], file_path: Path) -> None:
    """
    Save dictionary to JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path to save the JSON file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved JSON to {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {str(e)}")
        raise


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON file into dictionary.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Dict[str, Any]: Loaded JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {str(e)}")
        raise


def save_classes(classes: List[str], file_path: Path) -> None:
    """
    Save class names to JSON file.
    
    Args:
        classes: List of class names
        file_path: Path to save classes.json
    """
    class_data = {
        "classes": classes,
        "num_classes": len(classes),
        "created_at": datetime.now().isoformat()
    }
    save_json(class_data, file_path)


def load_classes(file_path: Path) -> List[str]:
    """
    Load class names from JSON file.
    
    Args:
        file_path: Path to classes.json
    
    Returns:
        List[str]: List of class names
    """
    data = load_json(file_path)
    return data.get("classes", [])


def parse_class_name(class_name: str) -> Tuple[str, str]:
    """
    Parse class name in format 'Crop___Disease' into crop and disease.
    
    Args:
        class_name: Class name in format 'Crop___Disease' or 'Crop___Healthy'
    
    Returns:
        Tuple[str, str]: (crop, disease) tuple
    
    Example:
        >>> parse_class_name("Tomato___Late_Blight")
        ("Tomato", "Late Blight")
        >>> parse_class_name("Tomato___Healthy")
        ("Tomato", "Healthy")
    """
    parts = class_name.split('___')
    
    if len(parts) == 2:
        crop = parts[0].replace('_', ' ')
        disease = parts[1].replace('_', ' ')
        return crop, disease
    else:
        # If format is unexpected, return as-is
        return class_name, "Unknown"


def format_class_name(crop: str, disease: str) -> str:
    """
    Format crop and disease into class name format.
    
    Args:
        crop: Crop name
        disease: Disease name
    
    Returns:
        str: Formatted class name 'Crop___Disease'
    """
    return f"{crop.replace(' ', '_')}___{disease.replace(' ', '_')}"


def get_severity(confidence: float, threshold: float = 0.70) -> str:
    """
    Determine disease severity based on confidence.
    
    Args:
        confidence: Prediction confidence (0-1)
        threshold: Confidence threshold (default: 0.70)
    
    Returns:
        str: Severity level ('High', 'Medium', 'Low', or 'Unknown')
    """
    if confidence < threshold:
        return "Unknown"
    elif confidence >= 0.90:
        return "High"
    elif confidence >= 0.80:
        return "Medium"
    else:
        return "Low"


def get_recommendations(crop: str, disease: str) -> List[str]:
    """
    Generate treatment recommendations based on crop and disease.
    
    Args:
        crop: Crop name
        disease: Disease name
    
    Returns:
        List[str]: List of recommendations
    """
    # Default recommendations
    recommendations = [
        "Consult with local agricultural extension officer",
        "Monitor the plant regularly for disease progression",
        "Ensure proper spacing between plants for air circulation",
        "Avoid overhead irrigation to reduce leaf wetness"
    ]
    
    # Disease-specific recommendations
    disease_lower = disease.lower()
    
    if "blight" in disease_lower:
        recommendations.extend([
            "Apply copper-based fungicides as preventive measure",
            "Remove and destroy infected plant parts",
            "Improve drainage in the field"
        ])
    elif "rust" in disease_lower:
        recommendations.extend([
            "Apply fungicides containing mancozeb or propiconazole",
            "Use rust-resistant varieties in future plantings",
            "Avoid working in fields when plants are wet"
        ])
    elif "mold" in disease_lower or "mildew" in disease_lower:
        recommendations.extend([
            "Apply sulfur or copper-based fungicides",
            "Reduce humidity around plants",
            "Increase air circulation through pruning"
        ])
    elif "spot" in disease_lower:
        recommendations.extend([
            "Apply appropriate fungicides (chlorothalonil or mancozeb)",
            "Remove infected leaves to prevent spread",
            "Avoid wetting leaves during irrigation"
        ])
    elif "virus" in disease_lower or "viral" in disease_lower:
        recommendations.extend([
            "Remove and destroy infected plants immediately",
            "Control insect vectors (aphids, whiteflies)",
            "Use virus-free seeds and resistant varieties"
        ])
    elif "rot" in disease_lower:
        recommendations.extend([
            "Improve soil drainage",
            "Avoid overwatering",
            "Apply appropriate fungicides to soil"
        ])
    elif "wilt" in disease_lower:
        recommendations.extend([
            "Remove infected plants to prevent spread",
            "Soil solarization may help reduce pathogen load",
            "Use resistant varieties"
        ])
    elif "healthy" in disease_lower:
        recommendations = [
            "Continue current care practices",
            "Monitor regularly for early disease detection",
            "Maintain proper fertilization and irrigation schedule"
        ]
    
    return recommendations


def preprocess_image(
    image: Image.Image,
    target_size: Tuple[int, int] = (224, 224)
) -> np.ndarray:
    """
    Preprocess image for model input.
    
    Args:
        image: PIL Image object
        target_size: Target size (height, width)
    
    Returns:
        np.ndarray: Preprocessed image array
    """
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Normalize to [0, 1]
    img_array = img_array.astype(np.float32) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def load_and_preprocess_image(
    image_path: Path,
    target_size: Tuple[int, int] = (224, 224)
) -> np.ndarray:
    """
    Load image from path and preprocess for model input.
    
    Args:
        image_path: Path to image file
        target_size: Target size (height, width)
    
    Returns:
        np.ndarray: Preprocessed image array
    """
    try:
        image = Image.open(image_path)
        return preprocess_image(image, target_size)
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {str(e)}")
        raise


class Timer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str):
        """
        Initialize timer.
        
        Args:
            operation_name: Name of the operation being timed
        """
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """Start timer."""
        self.start_time = time.time()
        logger.info(f"Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timer and log duration."""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        logger.info(f"Completed: {self.operation_name} in {duration:.2f} seconds")
        return False
    
    def get_duration(self) -> float:
        """
        Get duration in seconds.
        
        Returns:
            float: Duration in seconds
        """
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0


def validate_image_file(file_path: Path) -> bool:
    """
    Validate if file is a valid image.
    
    Args:
        file_path: Path to file
    
    Returns:
        bool: True if valid image, False otherwise
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_image_files(directory: Path) -> List[Path]:
    """
    Get all image files from directory.
    
    Args:
        directory: Directory path
    
    Returns:
        List[Path]: List of image file paths
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(directory.glob(f"*{ext}"))
        image_files.extend(directory.glob(f"*{ext.upper()}"))
    
    return sorted(image_files)


def print_system_info() -> None:
    """Print system information for debugging."""
    import platform
    import sys
    
    logger.info("=" * 50)
    logger.info("System Information")
    logger.info("=" * 50)
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Working Directory: {Path.cwd()}")
    logger.info("=" * 50)