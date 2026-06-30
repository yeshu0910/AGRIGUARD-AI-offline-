"""
Model architecture module for AgriGuard AI crop disease detection system.

This module implements the EfficientNetB0-based model with transfer learning
for crop disease classification.
"""

import logging
from pathlib import Path
from typing import Tuple, Optional, List

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

from ml_pipeline.config import get_config
from ml_pipeline.utils import logger


class CropDiseaseModel:
    """
    Crop disease detection model based on EfficientNetB0.
    
    Implements transfer learning with two-phase training:
    1. Train only the classification head
    2. Fine-tune the base model
    """
    
    def __init__(self, num_classes: int, input_shape: Tuple[int, int, int] = (224, 224, 3)):
        """
        Initialize model.
        
        Args:
            num_classes: Number of output classes
            input_shape: Input image shape (height, width, channels)
        """
        self.config = get_config()
        self.num_classes = num_classes
        self.input_shape = input_shape
        
        self.model: Optional[keras.Model] = None
        self.base_model: Optional[keras.Model] = None
        self.history = None
        
        logger.info(f"CropDiseaseModel initialized with {num_classes} classes")
    
    def build_model(self, freeze_base: bool = True) -> keras.Model:
        """
        Build the model architecture with EfficientNetB0 base.
        
        Args:
            freeze_base: If True, freeze the base model layers initially
        
        Returns:
            keras.Model: Compiled model
        """
        logger.info("Building model architecture...")
        
        # Input layer
        inputs = keras.Input(shape=self.input_shape)
        
        # Preprocess input for EfficientNet
        x = preprocess_input(inputs)
        
        # Load EfficientNetB0 base model
        self.base_model = EfficientNetB0(
            include_top=False,
            weights=self.config.model.WEIGHTS,
            input_tensor=x,
            pooling='avg'
        )
        
        # Freeze base model if requested
        if freeze_base:
            self.base_model.trainable = False
            logger.info("Base model frozen for initial training")
        else:
            logger.info("Base model will be fine-tuned")
        
        # Add custom classification head
        x = self.base_model.output
        
        # Add dropout for regularization
        x = layers.Dropout(0.3, name='dropout_1')(x)
        
        # First dense layer
        x = layers.Dense(512, activation='relu', name='dense_1')(x)
        x = layers.BatchNormalization(name='bn_1')(x)
        x = layers.Dropout(0.4, name='dropout_2')(x)
        
        # Second dense layer
        x = layers.Dense(256, activation='relu', name='dense_2')(x)
        x = layers.BatchNormalization(name='bn_2')(x)
        x = layers.Dropout(0.3, name='dropout_3')(x)
        
        # Output layer
        outputs = layers.Dense(
            self.num_classes,
            activation='softmax',
            name='output'
        )(x)
        
        # Create model
        self.model = models.Model(inputs=inputs, outputs=outputs, name='AgriGuardCropDisease')
        
        # Compile model
        self._compile_model(learning_rate=self.config.training.LEARNING_RATE)
        
        # Print model summary
        self.model.summary(print_fn=logger.info)
        
        logger.info("Model built successfully!")
        
        return self.model
    
    def _compile_model(self, learning_rate: float) -> None:
        """
        Compile the model with optimizer and loss function.
        
        Args:
            learning_rate: Learning rate for optimizer
        """
        optimizer = optimizers.Adam(learning_rate=learning_rate)
        
        self.model.compile(
            optimizer=optimizer,
            loss=self.config.training.LOSS,
            metrics=[
                'accuracy',
                keras.metrics.SparseTopKCategoricalAccuracy(k=5, name='top_5_accuracy'),
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall'),
                keras.metrics.AUC(name='auc')
            ]
        )
        
        logger.info(f"Model compiled with learning rate: {learning_rate}")
    
    def unfreeze_layers(self, num_layers: Optional[int] = None) -> None:
        """
        Unfreeze layers for fine-tuning.
        
        Args:
            num_layers: Number of layers to unfreeze from the top.
                       If None, unfreeze all layers.
        """
        if not self.base_model:
            raise ValueError("Model not built. Call build_model() first.")
        
        num_layers = num_layers or self.config.model.UNFREEZE_LAYERS
        
        # Unfreeze the top N layers
        self.base_model.trainable = True
        
        # Freeze all layers except the top N
        for layer in self.base_model.layers[:-num_layers]:
            layer.trainable = False
        
        logger.info(f"Unfroze top {num_layers} layers for fine-tuning")
        
        # Recompile with lower learning rate
        self._compile_model(learning_rate=self.config.training.FINE_TUNE_LR)
    
    def get_callbacks(self) -> List[callbacks.Callback]:
        """
        Create training callbacks.
        
        Returns:
            List[callbacks.Callback]: List of Keras callbacks
        """
        callback_list = []
        
        # Early stopping
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=self.config.training.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1
        )
        callback_list.append(early_stopping)
        
        # Reduce learning rate on plateau
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=self.config.training.REDUCE_LR_FACTOR,
            patience=self.config.training.REDUCE_LR_PATIENCE,
            min_lr=self.config.training.MIN_LR,
            verbose=1
        )
        callback_list.append(reduce_lr)
        
        # Model checkpoint
        checkpoint = callbacks.ModelCheckpoint(
            filepath=str(self.config.paths.CHECKPOINTS_DIR / 'best_model.keras'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
        callback_list.append(checkpoint)
        
        # TensorBoard
        tensorboard = callbacks.TensorBoard(
            log_dir=str(self.config.paths.TENSORBOARD_DIR),
            histogram_freq=1,
            write_graph=True,
            write_images=True
        )
        callback_list.append(tensorboard)
        
        logger.info(f"Created {len(callback_list)} callbacks")
        
        return callback_list
    
    def train(
        self,
        train_generator,
        val_generator,
        initial_epochs: Optional[int] = None,
        fine_tune_epochs: Optional[int] = None
    ) -> Tuple[keras.callbacks.History, keras.callbacks.History]:
        """
        Train the model with two-phase approach.
        
        Args:
            train_generator: Training data generator
            val_generator: Validation data generator
            initial_epochs: Number of epochs for initial training
            fine_tune_epochs: Number of epochs for fine-tuning
        
        Returns:
            Tuple[History, History]: Training histories for both phases
        """
        initial_epochs = initial_epochs or self.config.training.INITIAL_EPOCHS
        fine_tune_epochs = fine_tune_epochs or self.config.training.FINE_TUNE_EPOCHS
        
        callbacks_list = self.get_callbacks()
        
        # Phase 1: Train with frozen base model
        logger.info("=" * 60)
        logger.info("Phase 1: Training classification head")
        logger.info("=" * 60)
        
        history_initial = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=initial_epochs,
            callbacks=callbacks_list,
            verbose=1
        )
        
        # Phase 2: Fine-tune with unfrozen layers
        logger.info("=" * 60)
        logger.info("Phase 2: Fine-tuning with unfrozen layers")
        logger.info("=" * 60)
        
        self.unfreeze_layers()
        
        history_fine_tune = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=fine_tune_epochs,
            callbacks=callbacks_list,
            verbose=1,
            initial_epoch=len(history_initial.history['loss'])
        )
        
        # Combine histories
        self.history = self._combine_histories(history_initial, history_fine_tune)
        
        logger.info("Training completed successfully!")
        
        return history_initial, history_fine_tune
    
    def _combine_histories(
        self,
        history1: keras.callbacks.History,
        history2: keras.callbacks.History
    ) -> keras.callbacks.History:
        """
        Combine two training histories.
        
        Args:
            history1: First training history
            history2: Second training history
        
        Returns:
            keras.callbacks.History: Combined history
        """
        combined_history = keras.callbacks.History()
        
        # Combine metrics
        for key in history1.history.keys():
            combined_history.history[key] = (
                history1.history[key] + history2.history[key]
            )
        
        return combined_history
    
    def save_model(self, file_path: Optional[Path] = None) -> None:
        """
        Save model to file.
        
        Args:
            file_path: Path to save model. If None, uses config default.
        """
        if not self.model:
            raise ValueError("Model not built. Call build_model() first.")
        
        file_path = file_path or self.config.paths.MODEL_PATH
        
        self.model.save(file_path)
        logger.info(f"Model saved to {file_path}")
    
    def load_model(self, file_path: Optional[Path] = None) -> keras.Model:
        """
        Load model from file.
        
        Args:
            file_path: Path to model file. If None, uses config default.
        
        Returns:
            keras.Model: Loaded model
        """
        file_path = file_path or self.config.paths.MODEL_PATH
        
        if not file_path.exists():
            raise FileNotFoundError(f"Model file not found: {file_path}")
        
        self.model = keras.models.load_model(file_path)
        logger.info(f"Model loaded from {file_path}")
        
        return self.model
    
    def get_model_info(self) -> dict:
        """
        Get model information.
        
        Returns:
            dict: Model information dictionary
        """
        if not self.model:
            raise ValueError("Model not built. Call build_model() first.")
        
        total_params = self.model.count_params()
        trainable_params = sum(
            [np.prod(v.get_shape()) for v in self.model.trainable_weights]
        )
        non_trainable_params = total_params - trainable_params
        
        return {
            "total_params": int(total_params),
            "trainable_params": int(trainable_params),
            "non_trainable_params": int(non_trainable_params),
            "num_classes": self.num_classes,
            "input_shape": self.input_shape,
            "base_model": self.config.model.BASE_MODEL
        }


def create_model(num_classes: int, input_shape: Tuple[int, int, int] = (224, 224, 3)) -> CropDiseaseModel:
    """
    Factory function to create and build model.
    
    Args:
        num_classes: Number of output classes
        input_shape: Input image shape
    
    Returns:
        CropDiseaseModel: Initialized model instance
    """
    model = CropDiseaseModel(num_classes=num_classes, input_shape=input_shape)
    model.build_model(freeze_base=True)
    
    return model