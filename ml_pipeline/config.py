"""
Configuration module for AgriGuard AI crop disease detection system.

This module contains all configuration parameters for the ML pipeline,
including model settings, training parameters, and file paths.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class ModelConfig:
    """Model architecture configuration."""

    # Image dimensions
    IMG_SIZE: int = 224
    CHANNELS: int = 3

    # Model architecture
    BASE_MODEL: str = "EfficientNetB0"
    INPUT_SHAPE: Tuple[int, int, int] = (224, 224, 3)

    # Transfer learning
    WEIGHTS: str = "imagenet"
    FREEZE_BASE: bool = True
    UNFREEZE_LAYERS: int = 100  # Number of layers to unfreeze for fine-tuning


@dataclass
class TrainingConfig:
    """Training configuration."""

    # Dataset split
    TRAIN_SPLIT: float = 0.8
    VAL_SPLIT: float = 0.2

    # Training parameters
    BATCH_SIZE: int = 32
    INITIAL_EPOCHS: int = 20
    FINE_TUNE_EPOCHS: int = 15
    LEARNING_RATE: float = 0.001
    FINE_TUNE_LR: float = 0.0001

    # Class weights for imbalanced datasets
    CLASS_WEIGHTS: bool = True

    # Loss and optimizer
    LOSS: str = "sparse_categorical_crossentropy"
    OPTIMIZER: str = "adam"

    # Callbacks
    EARLY_STOPPING_PATIENCE: int = 5
    REDUCE_LR_PATIENCE: int = 3
    REDUCE_LR_FACTOR: float = 0.2
    MIN_LR: float = 1e-7


@dataclass
class AugmentationConfig:
    """Data augmentation configuration."""

    RANDOM_FLIP: str = "horizontal"
    RANDOM_ROTATION: float = 0.2
    RANDOM_ZOOM: float = 0.2
    RANDOM_CONTRAST: float = 0.2
    RANDOM_BRIGHTNESS: float = 0.2


@dataclass
class PathConfig:
    """File path configuration."""

    # Base directories
    BASE_DIR: Path = Path(__file__).parent.parent.resolve()
    DATASET_DIR: Path = BASE_DIR / "dataset"
    MODELS_DIR: Path = BASE_DIR / "models"
    OUTPUT_DIR: Path = BASE_DIR / "output"

    # Model files
    MODEL_PATH: Path = MODELS_DIR / "agriguard_model.keras"
    CLASSES_JSON: Path = MODELS_DIR / "classes.json"
    HISTORY_JSON: Path = OUTPUT_DIR / "training_history.json"
    METRICS_JSON: Path = OUTPUT_DIR / "training_metrics.json"

    # Output directories
    PLOTS_DIR: Path = OUTPUT_DIR / "plots"
    TENSORBOARD_DIR: Path = OUTPUT_DIR / "tensorboard"
    CHECKPOINTS_DIR: Path = OUTPUT_DIR / "checkpoints"

    def __post_init__(self):
        """Create directories if they don't exist."""
        for attr in [
            self.MODELS_DIR,
            self.OUTPUT_DIR,
            self.PLOTS_DIR,
            self.TENSORBOARD_DIR,
            self.CHECKPOINTS_DIR,
        ]:
            attr.mkdir(parents=True, exist_ok=True)


@dataclass
class PredictionConfig:
    """Prediction configuration."""

    CONFIDENCE_THRESHOLD: float = 0.70
    TOP_K_PREDICTIONS: int = 5
    GENERATE_GRADCAM: bool = True
    GENERATE_SALIENCY: bool = False


@dataclass
class Config:
    """Main configuration class combining all configs."""

    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    augmentation: AugmentationConfig = field(default_factory=AugmentationConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    prediction: PredictionConfig = field(default_factory=PredictionConfig)


# Global config instance
config = Config()


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config: Global configuration object
    """
    return config


def update_config(**kwargs) -> None:
    """
    Update configuration parameters.

    Args:
        **kwargs: Configuration parameters to update
    """
    global config

    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            raise ValueError(f"Unknown configuration parameter: {key}")
