"""
Training pipeline module for AgriGuard AI crop disease detection system.

This module orchestrates the complete training workflow including data loading,
model training, evaluation, and artifact saving.
"""

import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import time

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, precision_recall_fscore_support,
    top_k_accuracy_score
)

from ml_pipeline.config import get_config
from ml_pipeline.utils import (
    logger, save_json, Timer, print_system_info
)
from ml_pipeline.dataset_loader import DatasetLoader, validate_dataset_structure
from ml_pipeline.model import create_model


class Trainer:
    """
    Training pipeline for crop disease detection model.
    
    Orchestrates the complete training workflow from data loading to model export.
    """
    
    def __init__(self, dataset_dir: Optional[Path] = None):
        """
        Initialize trainer.
        
        Args:
            dataset_dir: Path to dataset directory. If None, uses config default.
        """
        self.config = get_config()
        self.dataset_dir = dataset_dir or self.config.paths.DATASET_DIR
        
        self.dataset_loader: Optional[DatasetLoader] = None
        self.model_wrapper = None
        self.model = None
        
        self.train_generator = None
        self.val_generator = None
        self.class_names = []
        
        self.history_initial = None
        self.history_fine_tune = None
        
        logger.info("Trainer initialized")
    
    def setup(self) -> None:
        """Set up training environment."""
        logger.info("=" * 60)
        logger.info("Setting up training environment")
        logger.info("=" * 60)
        
        # Print system info
        print_system_info()
        
        # Validate dataset
        if not validate_dataset_structure(self.dataset_dir):
            raise ValueError(f"Invalid dataset structure at {self.dataset_dir}")
        
        # Initialize dataset loader
        self.dataset_loader = DatasetLoader(self.dataset_dir)
        
        # Discover classes
        self.class_names = self.dataset_loader.discover_classes()
        num_classes = len(self.class_names)
        
        logger.info(f"Number of classes: {num_classes}")
        
        # Create model
        self.model_wrapper = create_model(
            num_classes=num_classes,
            input_shape=self.config.model.INPUT_SHAPE
        )
        self.model = self.model_wrapper.model
        
        # Print dataset info
        self.dataset_loader.print_dataset_info()
    
    def load_data(self) -> None:
        """Load and prepare dataset."""
        logger.info("Loading dataset...")
        
        with Timer("Dataset loading"):
            self.train_generator, self.val_generator = self.dataset_loader.load_dataset()
        
        logger.info("Dataset loaded successfully!")
    
    def train(self) -> None:
        """Execute training pipeline."""
        logger.info("=" * 60)
        logger.info("Starting training pipeline")
        logger.info("=" * 60)
        
        with Timer("Complete training"):
            self.history_initial, self.history_fine_tune = self.model_wrapper.train(
                self.train_generator,
                self.val_generator
            )
        
        logger.info("Training completed successfully!")
    
    def evaluate(self) -> Dict[str, Any]:
        """
        Evaluate model and generate metrics.
        
        Returns:
            Dict[str, Any]: Evaluation metrics
        """
        logger.info("=" * 60)
        logger.info("Evaluating model")
        logger.info("=" * 60)
        
        with Timer("Model evaluation"):
            # Get validation predictions
            val_generator = self.val_generator
            y_true = val_generator.classes
            y_pred_probs = self.model.predict(val_generator, verbose=1)
            y_pred = np.argmax(y_pred_probs, axis=1)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_true, y_pred, y_pred_probs)
            
            # Generate plots
            self._plot_training_history()
            self._plot_confusion_matrix(y_true, y_pred)
            self._plot_classification_report(y_true, y_pred)
            
            # Save metrics
            save_json(metrics, self.config.paths.METRICS_JSON)
            logger.info(f"Metrics saved to {self.config.paths.METRICS_JSON}")
        
        return metrics
    
    def _calculate_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_probs: np.ndarray
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_probs: Prediction probabilities
        
        Returns:
            Dict[str, Any]: Metrics dictionary
        """
        logger.info("Calculating metrics...")
        
        # Basic metrics
        loss, accuracy, top_5_accuracy, precision, recall, auc = self.model.evaluate(
            self.val_generator, verbose=0
        )
        
        # Per-class metrics
        precision_per_class, recall_per_class, f1_per_class, support_per_class = \
            precision_recall_fscore_support(y_true, y_pred, average=None)
        
        # Macro averages
        precision_macro, recall_macro, f1_macro, _ = \
            precision_recall_fscore_support(y_true, y_pred, average='macro')
        
        # Weighted averages
        precision_weighted, recall_weighted, f1_weighted, _ = \
            precision_recall_fscore_support(y_true, y_pred, average='weighted')
        
        # Top-5 accuracy
        top_5_acc = top_k_accuracy_score(y_true, y_pred_probs, k=5)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Classification report
        class_report = classification_report(
            y_true, y_pred,
            target_names=self.class_names,
            output_dict=True
        )
        
        metrics = {
            "overall": {
                "loss": float(loss),
                "accuracy": float(accuracy),
                "top_5_accuracy": float(top_5_acc),
                "precision_macro": float(precision_macro),
                "recall_macro": float(recall_macro),
                "f1_macro": float(f1_macro),
                "precision_weighted": float(precision_weighted),
                "recall_weighted": float(recall_weighted),
                "f1_weighted": float(f1_weighted),
                "auc": float(auc)
            },
            "per_class": {},
            "confusion_matrix": cm.tolist(),
            "classification_report": class_report,
            "class_names": self.class_names
        }
        
        # Add per-class metrics
        for idx, class_name in enumerate(self.class_names):
            metrics["per_class"][class_name] = {
                "precision": float(precision_per_class[idx]),
                "recall": float(recall_per_class[idx]),
                "f1_score": float(f1_per_class[idx]),
                "support": int(support_per_class[idx])
            }
        
        # Log key metrics
        logger.info(f"Validation Loss: {loss:.4f}")
        logger.info(f"Validation Accuracy: {accuracy:.4f}")
        logger.info(f"Top-5 Accuracy: {top_5_acc:.4f}")
        logger.info(f"Precision (macro): {precision_macro:.4f}")
        logger.info(f"Recall (macro): {recall_macro:.4f}")
        logger.info(f"F1 Score (macro): {f1_macro:.4f}")
        
        return metrics
    
    def _plot_training_history(self) -> None:
        """Plot training and validation metrics."""
        if not self.model_wrapper.history:
            logger.warning("No training history available")
            return
        
        history = self.model_wrapper.history.history
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Training History', fontsize=16, fontweight='bold')
        
        # Accuracy
        axes[0, 0].plot(history['accuracy'], label='Training Accuracy', linewidth=2)
        axes[0, 0].plot(history['val_accuracy'], label='Validation Accuracy', linewidth=2)
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Loss
        axes[0, 1].plot(history['loss'], label='Training Loss', linewidth=2)
        axes[0, 1].plot(history['val_loss'], label='Validation Loss', linewidth=2)
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Top-5 Accuracy
        if 'top_5_accuracy' in history:
            axes[1, 0].plot(history['top_5_accuracy'], label='Training Top-5 Acc', linewidth=2)
            axes[1, 0].plot(history['val_top_5_accuracy'], label='Validation Top-5 Acc', linewidth=2)
            axes[1, 0].set_title('Top-5 Accuracy')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Top-5 Accuracy')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Learning Rate (if available)
        if 'lr' in history:
            axes[1, 1].plot(history['lr'], linewidth=2, color='orange')
            axes[1, 1].set_title('Learning Rate')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Learning Rate')
            axes[1, 1].set_yscale('log')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].axis('off')
        
        plt.tight_layout()
        plot_path = self.config.paths.PLOTS_DIR / 'training_history.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Training history plot saved to {plot_path}")
        plt.close()
    
    def _plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        """
        cm = confusion_matrix(y_true, y_pred)
        
        # Normalize confusion matrix
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        
        # Raw counts
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            ax=axes[0]
        )
        axes[0].set_title('Confusion Matrix (Counts)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Predicted Label', fontsize=12)
        axes[0].set_ylabel('True Label', fontsize=12)
        
        # Normalized
        sns.heatmap(
            cm_norm, annot=True, fmt='.2f', cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            ax=axes[1]
        )
        axes[1].set_title('Confusion Matrix (Normalized)', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Predicted Label', fontsize=12)
        axes[1].set_ylabel('True Label', fontsize=12)
        
        plt.tight_layout()
        plot_path = self.config.paths.PLOTS_DIR / 'confusion_matrix.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Confusion matrix saved to {plot_path}")
        plt.close()
    
    def _plot_classification_report(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Plot classification report as heatmap.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        """
        from sklearn.metrics import classification_report
        
        report = classification_report(
            y_true, y_pred,
            target_names=self.class_names,
            output_dict=True
        )
        
        # Extract per-class metrics
        metrics_data = []
        for class_name in self.class_names:
            if class_name in report:
                metrics_data.append([
                    report[class_name]['precision'],
                    report[class_name]['recall'],
                    report[class_name]['f1-score']
                ])
        
        metrics_array = np.array(metrics_data)
        
        fig, ax = plt.subplots(figsize=(10, max(8, len(self.class_names) * 0.5)))
        
        sns.heatmap(
            metrics_array,
            annot=True,
            fmt='.3f',
            cmap='RdYlGn',
            xticklabels=['Precision', 'Recall', 'F1-Score'],
            yticklabels=self.class_names,
            ax=ax,
            vmin=0,
            vmax=1,
            cbar_kws={'label': 'Score'}
        )
        
        ax.set_title('Classification Report', fontsize=14, fontweight='bold')
        ax.set_xlabel('Metric', fontsize=12)
        ax.set_ylabel('Class', fontsize=12)
        
        plt.tight_layout()
        plot_path = self.config.paths.PLOTS_DIR / 'classification_report.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Classification report plot saved to {plot_path}")
        plt.close()
    
    def save_artifacts(self) -> None:
        """Save all training artifacts."""
        logger.info("=" * 60)
        logger.info("Saving training artifacts")
        logger.info("=" * 60)
        
        with Timer("Saving artifacts"):
            # Save model
            self.model_wrapper.save_model()
            
            # Save training history
            if self.model_wrapper.history:
                history_dict = {
                    'history': self.model_wrapper.history.history,
                    'params': self.model_wrapper.history.params
                }
                save_json(history_dict, self.config.paths.HISTORY_JSON)
                logger.info(f"Training history saved to {self.config.paths.HISTORY_JSON}")
            
            # Save model info
            model_info = self.model_wrapper.get_model_info()
            save_json(model_info, self.config.paths.OUTPUT_DIR / 'model_info.json')
            logger.info(f"Model info saved to {self.config.paths.OUTPUT_DIR / 'model_info.json'}")
        
        logger.info("All artifacts saved successfully!")
    
    def run(self) -> Dict[str, Any]:
        """
        Execute complete training pipeline.
        
        Returns:
            Dict[str, Any]: Evaluation metrics
        """
        try:
            # Setup
            self.setup()
            
            # Load data
            self.load_data()
            
            # Train
            self.train()
            
            # Evaluate
            metrics = self.evaluate()
            
            # Save artifacts
            self.save_artifacts()
            
            logger.info("=" * 60)
            logger.info("Training pipeline completed successfully!")
            logger.info("=" * 60)
            
            return metrics
        
        except Exception as e:
            logger.error(f"Training pipeline failed: {str(e)}", exc_info=True)
            raise


def main():
    """Main entry point for training."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Train AgriGuard AI crop disease detection model'
    )
    parser.add_argument(
        '--dataset-dir',
        type=Path,
        default=None,
        help='Path to dataset directory (default: ./dataset)'
    )
    parser.add_argument(
        '--epochs-initial',
        type=int,
        default=None,
        help='Number of initial training epochs (default: 20)'
    )
    parser.add_argument(
        '--epochs-fine-tune',
        type=int,
        default=None,
        help='Number of fine-tuning epochs (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Create trainer
    trainer = Trainer(dataset_dir=args.dataset_dir)
    
    # Run training
    metrics = trainer.run()
    
    # Print final results
    logger.info("=" * 60)
    logger.info("Final Results")
    logger.info("=" * 60)
    logger.info(f"Validation Accuracy: {metrics['overall']['accuracy']:.4f}")
    logger.info(f"Top-5 Accuracy: {metrics['overall']['top_5_accuracy']:.4f}")
    logger.info(f"F1 Score (macro): {metrics['overall']['f1_macro']:.4f}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()