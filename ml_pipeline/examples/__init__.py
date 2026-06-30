"""
Examples for AgriGuard AI ML Pipeline.

This package contains example scripts demonstrating various use cases
of the crop disease detection system.
"""

__version__ = "1.0.0"

from ml_pipeline.examples.basic_usage import (
    example_train,
    example_predict,
    example_batch_predict,
    example_gradcam,
    example_custom_config,
)

__all__ = [
    'example_train',
    'example_predict',
    'example_batch_predict',
    'example_gradcam',
    'example_custom_config',
]