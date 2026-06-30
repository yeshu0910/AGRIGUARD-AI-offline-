"""
Dataset loader module for AgriGuard AI crop disease detection system.

This module handles loading images from the dataset directory, automatic class
detection, train/validation splitting, and data augmentation.
"""

import logging
from pathlib import Path
from typing import Tuple, List, Dict, Optional
import random

import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from ml_pipeline.config import get_config
from ml_pipeline.utils import logger, get_image_files, save_classes, load_classes

# Set random seeds for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


class DatasetLoader:
    """
    Dataset loader for crop disease detection.
    
    Automatically detects classes from dataset directory structure and
    provides train/validation data generators with augmentation.
    """
    
    def __init__(self, dataset_dir: Optional[Path] = None):
        """
        Initialize dataset loader.
        
        Args:
            dataset_dir: Path to dataset directory. If None, uses config default.
        """
        self.config = get_config()
        self.dataset_dir = dataset_dir or self.config.paths.DATASET_DIR
        
        self.class_names: List[str] = []
        self.num_classes: int = 0
        self.class_to_index: Dict[str, int] = {}
        
        self.train_generator = None
        self.val_generator = None
        
        logger.info(f"DatasetLoader initialized with dataset directory: {self.dataset_dir}")
    
    def discover_classes(self) -> List[str]:
        """
        Automatically discover class names from dataset directory.
        
        Returns:
            List[str]: Sorted list of class names (folder names)
        
        Raises:
            FileNotFoundError: If dataset directory doesn't exist
            ValueError: If no valid class directories found
        """
        if not self.dataset_dir.exists():
            raise FileNotFoundError(f"Dataset directory not found: {self.dataset_dir}")
        
        # Get all subdirectories
        class_dirs = [d for d in self.dataset_dir.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
        
        if not class_dirs:
            raise ValueError(f"No class directories found in {self.dataset_dir}")
        
        # Extract class names from directory names
        self.class_names = sorted([d.name for d in class_dirs])
        self.num_classes = len(self.class_names)
        
        # Create class to index mapping
        self.class_to_index = {name: idx for idx, name in enumerate(self.class_names)}
        
        logger.info(f"Discovered {self.num_classes} classes:")
        for idx, class_name in enumerate(self.class_names):
            logger.info(f"  {idx}: {class_name}")
        
        # Save classes to JSON
        save_classes(self.class_names, self.config.paths.CLASSES_JSON)
        logger.info(f"Classes saved to {self.config.paths.CLASSES_JSON}")
        
        return self.class_names
    
    def load_classes_from_json(self) -> List[str]:
        """
        Load class names from saved JSON file.
        
        Returns:
            List[str]: List of class names
        """
        self.class_names = load_classes(self.config.paths.CLASSES_JSON)
        self.num_classes = len(self.class_names)
        self.class_to_index = {name: idx for idx, name in enumerate(self.class_names)}
        
        logger.info(f"Loaded {self.num_classes} classes from {self.config.paths.CLASSES_JSON}")
        return self.class_names
    
    def create_data_generators(self) -> Tuple[ImageDataGenerator, ImageDataGenerator]:
        """
        Create train and validation data generators with augmentation.
        
        Returns:
            Tuple[ImageDataGenerator, ImageDataGenerator]: Train and validation generators
        """
        if not self.class_names:
            raise ValueError("Classes not discovered. Call discover_classes() first.")
        
        # Training data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=self.config.training.VAL_SPLIT,
            # Augmentation parameters
            horizontal_flip=self.config.augmentation.RANDOM_FLIP == "horizontal",
            vertical_flip=self.config.augmentation.RANDOM_FLIP == "vertical",
            rotation_range=self.config.augmentation.RANDOM_ROTATION * 180,  # Convert to degrees
            zoom_range=self.config.augmentation.RANDOM_ZOOM,
            brightness_range=[
                1 - self.config.augmentation.RANDOM_BRIGHTNESS,
                1 + self.config.augmentation.RANDOM_BRIGHTNESS
            ],
            contrast_range=[
                1 - self.config.augmentation.RANDOM_CONTRAST,
                1 + self.config.augmentation.RANDOM_CONTRAST
            ],
            fill_mode='nearest'
        )
        
        # Validation data (no augmentation, only rescaling)
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=self.config.training.VAL_SPLIT
        )
        
        logger.info("Data generators created with augmentation:")
        logger.info(f"  - Random flip: {self.config.augmentation.RANDOM_FLIP}")
        logger.info(f"  - Random rotation: ±{self.config.augmentation.RANDOM_ROTATION * 180:.0f}°")
        logger.info(f"  - Random zoom: ±{self.config.augmentation.RANDOM_ZOOM * 100:.0f}%")
        logger.info(f"  - Random contrast: ±{self.config.augmentation.RANDOM_CONTRAST * 100:.0f}%")
        logger.info(f"  - Random brightness: ±{self.config.augmentation.RANDOM_BRIGHTNESS * 100:.0f}%")
        
        return train_datagen, val_datagen
    
    def create_dataset(
        self,
        datagen: ImageDataGenerator,
        subset: str = 'training'
    ) -> tf.keras.preprocessing.image.DirectoryIterator:
        """
        Create dataset iterator from data generator.
        
        Args:
            datagen: ImageDataGenerator instance
            subset: 'training' or 'validation'
        
        Returns:
            DirectoryIterator: Dataset iterator
        """
        dataset = datagen.flow_from_directory(
            self.dataset_dir,
            target_size=(self.config.model.IMG_SIZE, self.config.model.IMG_SIZE),
            batch_size=self.config.training.BATCH_SIZE,
            class_mode='sparse',
            subset=subset,
            seed=RANDOM_SEED,
            shuffle=True if subset == 'training' else False
        )
        
        logger.info(f"Created {subset} dataset:")
        logger.info(f"  - Samples: {dataset.samples}")
        logger.info(f"  - Batch size: {dataset.batch_size}")
        logger.info(f"  - Steps per epoch: {dataset.samples // dataset.batch_size}")
        
        return dataset
    
    def load_dataset(self) -> Tuple[tf.keras.preprocessing.image.DirectoryIterator, 
                                     tf.keras.preprocessing.image.DirectoryIterator]:
        """
        Load complete dataset with train/validation split.
        
        Returns:
            Tuple[DirectoryIterator, DirectoryIterator]: Train and validation datasets
        """
        logger.info("Loading dataset...")
        
        # Discover classes if not already done
        if not self.class_names:
            self.discover_classes()
        
        # Create data generators
        train_datagen, val_datagen = self.create_data_generators()
        
        # Create datasets
        self.train_generator = self.create_dataset(train_datagen, subset='training')
        self.val_generator = self.create_dataset(val_datagen, subset='validation')
        
        logger.info("Dataset loaded successfully!")
        
        return self.train_generator, self.val_generator
    
    def get_class_distribution(self) -> Dict[str, int]:
        """
        Get distribution of samples per class.
        
        Returns:
            Dict[str, int]: Dictionary mapping class names to sample counts
        """
        if not self.train_generator:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        distribution = {}
        class_indices = self.train_generator.class_indices
        
        # Count samples per class
        for class_name, idx in class_indices.items():
            count = sum(1 for label in self.train_generator.labels if label == idx)
            distribution[class_name] = count
        
        return distribution
    
    def print_dataset_info(self) -> None:
        """Print detailed dataset information."""
        if not self.class_names:
            logger.warning("Classes not discovered yet.")
            return
        
        logger.info("=" * 60)
        logger.info("Dataset Information")
        logger.info("=" * 60)
        logger.info(f"Dataset directory: {self.dataset_dir}")
        logger.info(f"Number of classes: {self.num_classes}")
        logger.info(f"Classes: {', '.join(self.class_names)}")
        
        if self.train_generator:
            logger.info(f"Training samples: {self.train_generator.samples}")
            logger.info(f"Validation samples: {self.val_generator.samples}")
            logger.info(f"Batch size: {self.config.training.BATCH_SIZE}")
            logger.info(f"Image size: {self.config.model.IMG_SIZE}x{self.config.model.IMG_SIZE}")
        
        logger.info("=" * 60)


def validate_dataset_structure(dataset_dir: Path) -> bool:
    """
    Validate dataset directory structure.
    
    Args:
        dataset_dir: Path to dataset directory
    
    Returns:
        bool: True if valid structure, False otherwise
    """
    if not dataset_dir.exists():
        logger.error(f"Dataset directory does not exist: {dataset_dir}")
        return False
    
    if not dataset_dir.is_dir():
        logger.error(f"Dataset path is not a directory: {dataset_dir}")
        return False
    
    # Check for at least one class directory
    class_dirs = [d for d in dataset_dir.iterdir() 
                  if d.is_dir() and not d.name.startswith('.')]
    
    if not class_dirs:
        logger.error(f"No class directories found in {dataset_dir}")
        return False
    
    # Check for images in at least one class directory
    has_images = False
    for class_dir in class_dirs:
        images = get_image_files(class_dir)
        if images:
            has_images = True
            logger.info(f"Found {len(images)} images in {class_dir.name}")
            break
    
    if not has_images:
        logger.error(f"No images found in any class directory in {dataset_dir}")
        return False
    
    logger.info(f"Dataset structure validated successfully. Found {len(class_dirs)} classes.")
    return True


def count_dataset_samples(dataset_dir: Path) -> Dict[str, int]:
    """
    Count total samples in dataset.
    
    Args:
        dataset_dir: Path to dataset directory
    
    Returns:
        Dict[str, int]: Dictionary with 'total', 'train', 'val' counts
    """
    if not dataset_dir.exists():
        return {"total": 0, "train": 0, "val": 0}
    
    total_images = 0
    class_dirs = [d for d in dataset_dir.iterdir() 
                  if d.is_dir() and not d.name.startswith('.')]
    
    for class_dir in class_dirs:
        images = get_image_files(class_dir)
        total_images += len(images)
    
    # Apply train/val split
    train_count = int(total_images * 0.8)
    val_count = total_images - train_count
    
    return {
        "total": total_images,
        "train": train_count,
        "val": val_count
    }