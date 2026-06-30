"""
Basic usage examples for AgriGuard AI ML Pipeline.

This script demonstrates how to use the ML pipeline for training and prediction.
"""

from pathlib import Path
from PIL import Image


# Example 1: Train a model
def example_train():
    """Example: Train a crop disease detection model."""
    from ml_pipeline import DatasetLoader, create_model
    from ml_pipeline.config import get_config

    print("Example 1: Training a model")
    print("=" * 60)

    # Initialize dataset loader
    loader = DatasetLoader(dataset_dir=Path("dataset"))

    # Discover classes automatically
    classes = loader.discover_classes()
    print(f"Discovered {len(classes)} classes")

    # Load dataset
    train_gen, val_gen = loader.load_dataset()

    # Create model
    model_wrapper = create_model(num_classes=len(classes))

    # Train model
    history_initial, history_fine_tune = model_wrapper.train(
        train_gen, val_gen, initial_epochs=20, fine_tune_epochs=10
    )

    # Save model
    model_wrapper.save_model()

    print("Training completed!")
    print("=" * 60)


# Example 2: Make predictions
def example_predict():
    """Example: Make predictions on new images."""
    from ml_pipeline import create_predictor

    print("\nExample 2: Making predictions")
    print("=" * 60)

    # Load predictor
    predictor = create_predictor()

    # Load image
    image = Image.open("test_image.jpg")

    # Make prediction
    result = predictor.predict(image)

    # Display results
    print(f"Crop: {result['crop']}")
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Severity: {result['severity']}")
    print(f"\nRecommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")

    print("=" * 60)


# Example 3: Batch prediction
def example_batch_predict():
    """Example: Batch prediction on multiple images."""
    from ml_pipeline import create_predictor
    from pathlib import Path

    print("\nExample 3: Batch prediction")
    print("=" * 60)

    # Load predictor
    predictor = create_predictor()

    # Get all images in a directory
    image_dir = Path("test_images")
    image_paths = list(image_dir.glob("*.jpg"))

    # Run batch prediction
    results = predictor.predict_batch(image_paths)

    # Display results
    for img_path, result in zip(image_paths, results):
        print(f"\n{img_path.name}:")
        print(f"  Crop: {result['crop']}")
        print(f"  Disease: {result['disease']}")
        print(f"  Confidence: {result['confidence']:.2%}")

    print("=" * 60)


# Example 4: Grad-CAM visualization
def example_gradcam():
    """Example: Generate Grad-CAM visualization."""
    from ml_pipeline import create_predictor
    from PIL import Image

    print("\nExample 4: Grad-CAM visualization")
    print("=" * 60)

    # Load predictor
    predictor = create_predictor()

    # Load image
    image = Image.open("test_image.jpg")

    # Generate Grad-CAM
    gradcam = predictor.generate_gradcam(image)

    # Save visualization
    gradcam.save("gradcam_output.png")
    print("Grad-CAM saved to gradcam_output.png")

    print("=" * 60)


# Example 5: Custom configuration
def example_custom_config():
    """Example: Use custom configuration."""
    from ml_pipeline import DatasetLoader, create_model
    from ml_pipeline.config import get_config, update_config

    print("\nExample 5: Custom configuration")
    print("=" * 60)

    # Update configuration
    update_config(
        training__BATCH_SIZE=16,
        training__LEARNING_RATE=0.0005,
        prediction__CONFIDENCE_THRESHOLD=0.80,
    )

    # Use updated config
    config = get_config()
    print(f"Batch size: {config.training.BATCH_SIZE}")
    print(f"Learning rate: {config.training.LEARNING_RATE}")
    print(f"Confidence threshold: {config.prediction.CONFIDENCE_THRESHOLD}")

    print("=" * 60)


def main():
    """Run all examples."""
    print("AgriGuard AI ML Pipeline - Examples")
    print("=" * 60)

    examples = [
        ("Train Model", example_train),
        ("Make Predictions", example_predict),
        ("Batch Prediction", example_batch_predict),
        ("Grad-CAM Visualization", example_gradcam),
        ("Custom Configuration", example_custom_config),
    ]

    print("\nAvailable examples:")
    for idx, (name, _) in enumerate(examples, 1):
        print(f"  {idx}. {name}")

    print("\nTo run an example, call the corresponding function.")
    print("Note: Some examples require a trained model and dataset.")

    # Run a simple example
    print("\n" + "=" * 60)
    print("Running: Custom Configuration Example")
    print("=" * 60)
    example_custom_config()


if __name__ == "__main__":
    main()
