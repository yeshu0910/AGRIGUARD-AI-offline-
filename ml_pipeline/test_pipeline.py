"""
Test script for AgriGuard AI ML Pipeline.

This script performs basic validation of the ML pipeline components
without requiring a full dataset or trained model.
"""

import sys
from pathlib import Path
from typing import List, Tuple


def test_imports() -> Tuple[bool, List[str]]:
    """
    Test that all required modules can be imported.
    
    Returns:
        Tuple[bool, List[str]]: (success, failed_imports)
    """
    print("Testing imports...")
    failed = []
    
    # Test core dependencies
    try:
        import tensorflow as tf
        print(f"  ✅ TensorFlow {tf.__version__}")
    except ImportError as e:
        print(f"  ❌ TensorFlow: {e}")
        failed.append("tensorflow")
    
    try:
        import numpy as np
        print(f"  ✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"  ❌ NumPy: {e}")
        failed.append("numpy")
    
    try:
        from PIL import Image
        print(f"  ✅ Pillow")
    except ImportError as e:
        print(f"  ❌ Pillow: {e}")
        failed.append("Pillow")
    
    try:
        import matplotlib
        print(f"  ✅ Matplotlib {matplotlib.__version__}")
    except ImportError as e:
        print(f"  ❌ Matplotlib: {e}")
        failed.append("matplotlib")
    
    try:
        import seaborn as sns
        print(f"  ✅ Seaborn {sns.__version__}")
    except ImportError as e:
        print(f"  ❌ Seaborn: {e}")
        failed.append("seaborn")
    
    try:
        from sklearn.metrics import confusion_matrix
        print(f"  ✅ Scikit-learn")
    except ImportError as e:
        print(f"  ❌ Scikit-learn: {e}")
        failed.append("scikit-learn")
    
    # Test ml_pipeline modules
    print("\nTesting ml_pipeline modules...")
    
    try:
        from ml_pipeline import config
        print("  ✅ ml_pipeline.config")
    except ImportError as e:
        print(f"  ❌ ml_pipeline.config: {e}")
        failed.append("ml_pipeline.config")
    
    try:
        from ml_pipeline import utils
        print("  ✅ ml_pipeline.utils")
    except ImportError as e:
        print(f"  ❌ ml_pipeline.utils: {e}")
        failed.append("ml_pipeline.utils")
    
    try:
        from ml_pipeline import dataset_loader
        print("  ✅ ml_pipeline.dataset_loader")
    except ImportError as e:
        print(f"  ❌ ml_pipeline.dataset_loader: {e}")
        failed.append("ml_pipeline.dataset_loader")
    
    try:
        from ml_pipeline import model
        print("  ✅ ml_pipeline.model")
    except ImportError as e:
        print(f"  ❌ ml_pipeline.model: {e}")
        failed.append("ml_pipeline.model")
    
    try:
        from ml_pipeline import predict
        print("  ✅ ml_pipeline.predict")
    except ImportError as e:
        print(f"  ❌ ml_pipeline.predict: {e}")
        failed.append("ml_pipeline.predict")
    
    return len(failed) == 0, failed


def test_config() -> Tuple[bool, str]:
    """
    Test configuration module.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    print("\nTesting configuration...")
    
    try:
        from ml_pipeline.config import get_config, Config
        
        config = get_config()
        
        # Verify config attributes
        assert hasattr(config, 'model'), "Missing model config"
        assert hasattr(config, 'training'), "Missing training config"
        assert hasattr(config, 'augmentation'), "Missing augmentation config"
        assert hasattr(config, 'paths'), "Missing paths config"
        assert hasattr(config, 'prediction'), "Missing prediction config"
        
        # Verify specific values
        assert config.model.IMG_SIZE == 224, "Invalid IMG_SIZE"
        assert config.model.BASE_MODEL == "EfficientNetB0", "Invalid BASE_MODEL"
        assert config.training.BATCH_SIZE == 32, "Invalid BATCH_SIZE"
        assert config.training.INITIAL_EPOCHS == 20, "Invalid INITIAL_EPOCHS"
        assert config.training.FINE_TUNE_EPOCHS == 10, "Invalid FINE_TUNE_EPOCHS"
        assert config.prediction.CONFIDENCE_THRESHOLD == 0.70, "Invalid CONFIDENCE_THRESHOLD"
        
        print("  ✅ Configuration valid")
        return True, "Configuration test passed"
    
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False, str(e)


def test_utils() -> Tuple[bool, str]:
    """
    Test utility functions.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    print("\nTesting utilities...")
    
    try:
        from ml_pipeline.utils import (
            parse_class_name,
            format_class_name,
            get_severity,
            get_recommendations,
            Timer
        )
        
        # Test parse_class_name
        crop, disease = parse_class_name("Tomato___Late_Blight")
        assert crop == "Tomato", f"Invalid crop: {crop}"
        assert disease == "Late Blight", f"Invalid disease: {disease}"
        print("  ✅ parse_class_name works")
        
        # Test format_class_name
        formatted = format_class_name("Tomato", "Late Blight")
        assert formatted == "Tomato___Late_Blight", f"Invalid format: {formatted}"
        print("  ✅ format_class_name works")
        
        # Test get_severity
        assert get_severity(0.95) == "High", "Invalid severity for 0.95"
        assert get_severity(0.85) == "Medium", "Invalid severity for 0.85"
        assert get_severity(0.75) == "Low", "Invalid severity for 0.75"
        assert get_severity(0.50) == "Unknown", "Invalid severity for 0.50"
        print("  ✅ get_severity works")
        
        # Test get_recommendations
        recs = get_recommendations("Tomato", "Late Blight")
        assert len(recs) > 0, "No recommendations returned"
        assert isinstance(recs, list), "Recommendations not a list"
        print("  ✅ get_recommendations works")
        
        # Test Timer
        with Timer("test"):
            import time
            time.sleep(0.01)
        print("  ✅ Timer works")
        
        return True, "Utility tests passed"
    
    except Exception as e:
        print(f"  ❌ Utility test failed: {e}")
        return False, str(e)


def test_model_architecture() -> Tuple[bool, str]:
    """
    Test model architecture creation (without training).
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    print("\nTesting model architecture...")
    
    try:
        from ml_pipeline.model import create_model
        import tensorflow as tf
        
        # Create a small test model
        model_wrapper = create_model(num_classes=5, input_shape=(224, 224, 3))
        
        # Verify model
        assert model_wrapper.model is not None, "Model not created"
        assert model_wrapper.num_classes == 5, "Invalid num_classes"
        
        # Test prediction with dummy input
        dummy_input = tf.random.normal((1, 224, 224, 3))
        predictions = model_wrapper.model.predict(dummy_input, verbose=0)
        
        assert predictions.shape == (1, 5), f"Invalid prediction shape: {predictions.shape}"
        assert abs(predictions.sum() - 1.0) < 1e-5, "Predictions don't sum to 1"
        
        print("  ✅ Model architecture works")
        print(f"     - Parameters: {model_wrapper.model.count_params():,}")
        print(f"     - Input shape: {model_wrapper.input_shape}")
        print(f"     - Output shape: {predictions.shape}")
        
        return True, "Model architecture test passed"
    
    except Exception as e:
        print(f"  ❌ Model architecture test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)


def test_dataset_loader() -> Tuple[bool, str]:
    """
    Test dataset loader initialization.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    print("\nTesting dataset loader...")
    
    try:
        from ml_pipeline.dataset_loader import DatasetLoader, validate_dataset_structure
        from ml_pipeline.config import get_config
        
        config = get_config()
        
        # Test initialization
        loader = DatasetLoader(dataset_dir=config.paths.DATASET_DIR)
        assert loader.dataset_dir == config.paths.DATASET_DIR, "Invalid dataset_dir"
        print("  ✅ DatasetLoader initializes correctly")
        
        # Test validation function exists
        assert callable(validate_dataset_structure), "validate_dataset_structure not callable"
        print("  ✅ validate_dataset_structure function exists")
        
        return True, "Dataset loader test passed"
    
    except Exception as e:
        print(f"  ❌ Dataset loader test failed: {e}")
        return False, str(e)


def test_predictor() -> Tuple[bool, str]:
    """
    Test predictor initialization (without loading model).
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    print("\nTesting predictor...")
    
    try:
        from ml_pipeline.predict import CropDiseasePredictor, format_prediction_for_streamlit
        from ml_pipeline.config import get_config
        
        config = get_config()
        
        # Test initialization
        predictor = CropDiseasePredictor(
            model_path=config.paths.MODEL_PATH,
            classes_path=config.paths.CLASSES_JSON
        )
        
        assert predictor.model_path == config.paths.MODEL_PATH, "Invalid model_path"
        assert predictor.classes_path == config.paths.CLASSES_JSON, "Invalid classes_path"
        print("  ✅ CropDiseasePredictor initializes correctly")
        
        # Test format_prediction_for_streamlit
        test_result = {
            "crop": "Tomato",
            "disease": "Late Blight",
            "confidence": 0.95,
            "severity": "High",
            "recommendations": ["Test recommendation"],
            "top_5_predictions": [],
            "prediction_time": 0.123,
            "is_confident": True,
            "message": None
        }
        
        formatted = format_prediction_for_streamlit(test_result)
        assert formatted["crop"] == "Tomato", "Invalid formatted crop"
        assert formatted["confidence"] == "95.00%", "Invalid formatted confidence"
        print("  ✅ format_prediction_for_streamlit works")
        
        return True, "Predictor test passed"
    
    except Exception as e:
        print(f"  ❌ Predictor test failed: {e}")
        return False, str(e)


def run_all_tests() -> bool:
    """
    Run all tests and report results.
    
    Returns:
        bool: True if all tests passed
    """
    print("=" * 60)
    print("AgriGuard AI ML Pipeline - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Utilities", test_utils),
        ("Model Architecture", test_model_architecture),
        ("Dataset Loader", test_dataset_loader),
        ("Predictor", test_predictor)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if test_name == "Imports":
                success, data = test_func()
                results.append((test_name, success, f"Failed: {', '.join(data)}" if not success else "Passed"))
            else:
                success, message = test_func()
                results.append((test_name, success, message))
        except Exception as e:
            results.append((test_name, False, f"Exception: {str(e)}"))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, message in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Pipeline is ready.")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please review errors above.")
        return False


def main():
    """Main entry point."""
    success = run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()