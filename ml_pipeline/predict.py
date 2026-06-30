"""
Prediction module for AgriGuard AI crop disease detection system.

This module handles model inference, result parsing, confidence scoring,
and provides integration utilities for the Streamlit application.
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import time
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf

from ml_pipeline.config import get_config
from ml_pipeline.utils import (
    logger, load_json, parse_class_name, get_severity, 
    get_recommendations, preprocess_image, Timer
)


class CropDiseasePredictor:
    """
    Crop disease prediction engine.
    
    Loads trained model and performs inference on new images.
    Supports single and batch prediction with confidence scoring.
    """
    
    def __init__(
        self,
        model_path: Optional[Path] = None,
        classes_path: Optional[Path] = None
    ):
        """
        Initialize predictor.
        
        Args:
            model_path: Path to trained model file
            classes_path: Path to classes.json file
        """
        self.config = get_config()
        
        self.model_path = model_path or self.config.paths.MODEL_PATH
        self.classes_path = classes_path or self.config.paths.CLASSES_JSON
        
        self.model: Optional[tf.keras.Model] = None
        self.class_names: List[str] = []
        self.num_classes: int = 0
        
        logger.info("CropDiseasePredictor initialized")
    
    def load(self) -> None:
        """Load model and class names."""
        logger.info("Loading model and classes...")
        
        # Load model
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        self.model = tf.keras.models.load_model(self.model_path)
        logger.info(f"Model loaded from {self.model_path}")
        
        # Load classes
        if not self.classes_path.exists():
            raise FileNotFoundError(f"Classes file not found: {self.classes_path}")
        
        class_data = load_json(self.classes_path)
        self.class_names = class_data.get("classes", [])
        self.num_classes = len(self.class_names)
        
        logger.info(f"Loaded {self.num_classes} classes")
        logger.info(f"Classes: {', '.join(self.class_names)}")
    
    def predict(
        self,
        image: Union[Image.Image, Path, str],
        return_top_k: int = 5
    ) -> Dict[str, any]:
        """
        Predict crop disease from image.
        
        Args:
            image: PIL Image, Path, or file path string
            return_top_k: Number of top predictions to return
        
        Returns:
            Dict containing prediction results
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load() first.")
        
        start_time = time.time()
        
        # Load image if path provided
        if isinstance(image, (Path, str)):
            image = Image.open(image)
        
        # Preprocess image
        img_array = preprocess_image(image, target_size=(224, 224))
        
        # Run inference
        predictions = self.model.predict(img_array, verbose=0)[0]
        
        # Get top-k predictions
        top_indices = np.argsort(predictions)[::-1][:return_top_k]
        top_predictions = []
        
        for idx in top_indices:
            class_name = self.class_names[idx]
            confidence = float(predictions[idx])
            crop, disease = parse_class_name(class_name)
            
            top_predictions.append({
                "class_name": class_name,
                "crop": crop,
                "disease": disease,
                "confidence": confidence,
                "severity": get_severity(confidence)
            })
        
        # Get top prediction
        top_pred = top_predictions[0]
        
        # Determine if prediction is reliable
        is_confident = top_pred["confidence"] >= self.config.prediction.CONFIDENCE_THRESHOLD
        
        if is_confident:
            crop = top_pred["crop"]
            disease = top_pred["disease"]
            confidence = top_pred["confidence"]
            severity = top_pred["severity"]
            recommendations = get_recommendations(crop, disease)
            message = None
        else:
            crop = "Unknown"
            disease = "Unknown"
            confidence = top_pred["confidence"]
            severity = "Unknown"
            recommendations = [
                "Please upload a clearer image",
                "Ensure the image shows the affected plant part clearly",
                "Try capturing the image in good lighting conditions",
                "Include multiple angles of the affected area if possible"
            ]
            message = "Unknown crop or disease. Please upload a clearer image."
        
        # Calculate prediction time
        prediction_time = time.time() - start_time
        
        result = {
            "crop": crop,
            "disease": disease,
            "confidence": confidence,
            "severity": severity,
            "recommendations": recommendations,
            "top_5_predictions": top_predictions,
            "prediction_time": prediction_time,
            "is_confident": is_confident,
            "message": message
        }
        
        logger.info(f"Prediction completed in {prediction_time:.3f}s")
        logger.info(f"Top prediction: {crop} - {disease} ({confidence:.2%})")
        
        return result
    
    def predict_batch(
        self,
        images: List[Union[Image.Image, Path, str]]
    ) -> List[Dict[str, any]]:
        """
        Predict crop disease for multiple images.
        
        Args:
            images: List of PIL Images, Paths, or file path strings
        
        Returns:
            List of prediction result dictionaries
        """
        logger.info(f"Running batch prediction on {len(images)} images")
        
        results = []
        for idx, image in enumerate(images):
            logger.info(f"Processing image {idx + 1}/{len(images)}")
            result = self.predict(image)
            results.append(result)
        
        logger.info(f"Batch prediction completed for {len(images)} images")
        
        return results
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get model information.
        
        Returns:
            Dict containing model information
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load() first.")
        
        total_params = self.model.count_params()
        trainable_params = sum(
            [np.prod(v.get_shape()) for v in self.model.trainable_weights]
        )
        
        return {
            "total_params": int(total_params),
            "trainable_params": int(trainable_params),
            "num_classes": self.num_classes,
            "classes": self.class_names,
            "input_shape": (224, 224, 3),
            "confidence_threshold": self.config.prediction.CONFIDENCE_THRESHOLD
        }
    
    def generate_gradcam(
        self,
        image: Union[Image.Image, Path, str],
        class_idx: Optional[int] = None,
        layer_name: str = 'top_conv'
    ) -> Image.Image:
        """
        Generate Grad-CAM visualization for model explanation.
        
        Args:
            image: Input image
            class_idx: Class index to visualize. If None, uses top prediction.
            layer_name: Name of the last convolutional layer
        
        Returns:
            PIL Image with Grad-CAM overlay
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load() first.")
        
        # Load image if path provided
        if isinstance(image, (Path, str)):
            image = Image.open(image)
        
        # Preprocess image
        img_array = preprocess_image(image, target_size=(224, 224))
        
        # Get prediction if class_idx not provided
        if class_idx is None:
            predictions = self.model.predict(img_array, verbose=0)[0]
            class_idx = int(np.argmax(predictions))
        
        # Create gradient model
        grad_model = tf.keras.models.Model(
            [self.model.inputs],
            [self.model.get_layer(layer_name).output, self.model.output]
        )
        
        # Compute gradients
        with tf.GradientTape() as tape:
            conv_output, predictions = grad_model(img_array)
            class_channel = predictions[:, class_idx]
        
        grads = tape.gradient(class_channel, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Weight the channels by importance
        conv_output = conv_output[0]
        heatmap = conv_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalize heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        heatmap = heatmap.numpy()
        
        # Resize heatmap to match image size
        heatmap = Image.fromarray(np.uint8(255 * heatmap))
        heatmap = heatmap.resize((224, 224), Image.Resampling.BILINEAR)
        heatmap = np.array(heatmap)
        
        # Create colored heatmap
        heatmap_colored = plt_cm(heatmap)
        
        # Superimpose heatmap on original image
        original_img = image.resize((224, 224), Image.Resampling.LANCZOS)
        original_array = np.array(original_img) / 255.0
        
        superimposed = heatmap_colored[:, :, :3] * 0.4 + original_array * 0.6
        superimposed = np.clip(superimposed, 0, 1)
        
        # Convert to PIL Image
        superimposed_img = Image.fromarray(np.uint8(255 * superimposed))
        
        return superimposed_img
    
    def generate_saliency_map(
        self,
        image: Union[Image.Image, Path, str],
        class_idx: Optional[int] = None
    ) -> Image.Image:
        """
        Generate saliency map for model explanation.
        
        Args:
            image: Input image
            class_idx: Class index to visualize. If None, uses top prediction.
        
        Returns:
            PIL Image with saliency map
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load() first.")
        
        # Load image if path provided
        if isinstance(image, (Path, str)):
            image = Image.open(image)
        
        # Preprocess image
        img_array = preprocess_image(image, target_size=(224, 224))
        img_tensor = tf.convert_to_tensor(img_array)
        
        # Get prediction if class_idx not provided
        if class_idx is None:
            predictions = self.model.predict(img_array, verbose=0)[0]
            class_idx = int(np.argmax(predictions))
        
        # Compute saliency
        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            predictions = self.model(img_tensor)
            class_score = predictions[:, class_idx]
        
        # Compute gradients
        saliency = tape.gradient(class_score, img_tensor)
        saliency = tf.abs(saliency)
        saliency = tf.reduce_max(saliency, axis=-1)
        saliency = saliency[0].numpy()
        
        # Normalize
        saliency = (saliency - saliency.min()) / (saliency.max() - saliency.min() + 1e-8)
        
        # Create colored saliency map
        saliency_colored = plt_cm(saliency)
        
        # Superimpose on original image
        original_img = image.resize((224, 224), Image.Resampling.LANCZOS)
        original_array = np.array(original_img) / 255.0
        
        superimposed = saliency_colored[:, :, :3] * 0.5 + original_array * 0.5
        superimposed = np.clip(superimposed, 0, 1)
        
        # Convert to PIL Image
        superimposed_img = Image.fromarray(np.uint8(255 * superimposed))
        
        return superimposed_img


def plt_cm(arr: np.ndarray) -> np.ndarray:
    """
    Apply colormap to array.
    
    Args:
        arr: 2D numpy array
    
    Returns:
        np.ndarray: Colored array
    """
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap('jet')
    return cmap(arr)


def format_prediction_for_streamlit(result: Dict[str, any]) -> Dict[str, any]:
    """
    Format prediction result for Streamlit display.
    
    Args:
        result: Raw prediction result from predictor
    
    Returns:
        Dict formatted for Streamlit
    """
    return {
        "crop": result["crop"],
        "disease": result["disease"],
        "confidence": f"{result['confidence']:.2%}",
        "confidence_raw": result["confidence"],
        "severity": result["severity"],
        "recommendations": result["recommendations"],
        "top_5": result["top_5_predictions"],
        "prediction_time": f"{result['prediction_time']:.3f}s",
        "is_confident": result["is_confident"],
        "message": result["message"]
    }


def create_predictor(
    model_path: Optional[Path] = None,
    classes_path: Optional[Path] = None
) -> CropDiseasePredictor:
    """
    Factory function to create and load predictor.
    
    Args:
        model_path: Path to model file
        classes_path: Path to classes.json
    
    Returns:
        CropDiseasePredictor: Loaded predictor instance
    """
    predictor = CropDiseasePredictor(model_path, classes_path)
    predictor.load()
    return predictor


def predict_from_file(
    image_path: Union[Path, str],
    model_path: Optional[Path] = None,
    classes_path: Optional[Path] = None
) -> Dict[str, any]:
    """
    Convenience function to predict from image file.
    
    Args:
        image_path: Path to image file
        model_path: Path to model file (optional)
        classes_path: Path to classes.json (optional)
    
    Returns:
        Dict: Prediction result
    """
    predictor = create_predictor(model_path, classes_path)
    result = predictor.predict(image_path)
    return result


def main():
    """Main entry point for prediction."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Predict crop disease from image'
    )
    parser.add_argument(
        'image_path',
        type=Path,
        help='Path to image file'
    )
    parser.add_argument(
        '--model',
        type=Path,
        default=None,
        help='Path to model file (default: ./models/agriguard_model.keras)'
    )
    parser.add_argument(
        '--classes',
        type=Path,
        default=None,
        help='Path to classes.json (default: ./models/classes.json)'
    )
    parser.add_argument(
        '--gradcam',
        action='store_true',
        help='Generate Grad-CAM visualization'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Path to save Grad-CAM visualization'
    )
    
    args = parser.parse_args()
    
    # Create predictor
    predictor = create_predictor(args.model, args.classes)
    
    # Run prediction
    result = predictor.predict(args.image_path)
    
    # Print results
    print("\n" + "=" * 60)
    print("Prediction Results")
    print("=" * 60)
    print(f"Crop: {result['crop']}")
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Severity: {result['severity']}")
    print(f"Prediction Time: {result['prediction_time']:.3f}s")
    print("\nTop 5 Predictions:")
    for idx, pred in enumerate(result['top_5_predictions'], 1):
        print(f"  {idx}. {pred['crop']} - {pred['disease']}: {pred['confidence']:.2%}")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    print("=" * 60)
    
    # Generate Grad-CAM if requested
    if args.gradcam:
        logger.info("Generating Grad-CAM visualization...")
        gradcam_img = predictor.generate_gradcam(args.image_path)
        
        output_path = args.output or Path('gradcam_output.png')
        gradcam_img.save(output_path)
        logger.info(f"Grad-CAM saved to {output_path}")


if __name__ == "__main__":
    main()