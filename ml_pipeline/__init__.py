"""
AgriGuard AI ML Pipeline

A production-ready, offline crop disease detection system using TensorFlow/Keras
and EfficientNetB0 for transfer learning.

Modules:
    - config: Configuration management
    - utils: Utility functions
    - dataset_loader: Dataset loading and preprocessing
    - model: Model architecture and training
    - train: Training pipeline
    - predict: Prediction and inference

Example:
    >>> from ml_pipeline import create_model, DatasetLoader
    >>> loader = DatasetLoader()
    >>> classes = loader.discover_classes()
    >>> model = create_model(num_classes=len(classes))
"""

__version__ = "1.0.0"
__author__ = "AgriGuard AI Team"

from ml_pipeline.config import get_config, Config
from ml_pipeline.utils import (
    setup_logging,
    save_json,
    load_json,
    parse_class_name,
    get_severity,
    get_recommendations,
    Timer
)
from ml_pipeline.dataset_loader import DatasetLoader, validate_dataset_structure
from ml_pipeline.model import CropDiseaseModel, create_model
from ml_pipeline.predict import CropDiseasePredictor, create_predictor

__all__ = [
    # Config
    'get_config',
    'Config',
    # Utils
    'setup_logging',
    'save_json',
    'load_json',
    'parse_class_name',
    'get_severity',
    'get_recommendations',
    'Timer',
    # Dataset
    'DatasetLoader',
    'validate_dataset_structure',
    # Model
    'CropDiseaseModel',
    'create_model',
    # Prediction
    'CropDiseasePredictor',
    'create_predictor'
]