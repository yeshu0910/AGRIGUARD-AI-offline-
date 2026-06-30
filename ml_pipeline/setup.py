"""
Setup script for AgriGuard AI ML Pipeline.

This script helps with initial setup, dataset validation, and environment checks.
"""

import sys
from pathlib import Path
from typing import List, Tuple


def check_python_version() -> bool:
    """
    Check if Python version meets requirements.

    Returns:
        bool: True if Python version is adequate
    """
    version = sys.version_info
    required = (3, 10)

    if version >= required:
        print(
            f"✅ Python {version.major}.{version.minor}.{version.micro} (>= {required[0]}.{required[1]})"
        )
        return True
    else:
        print(
            f"❌ Python {version.major}.{version.minor}.{version.micro} (< {required[0]}.{required[1]})"
        )
        print(f"   Please upgrade to Python {required[0]}.{required[1]} or higher")
        return False


def check_dependencies() -> Tuple[bool, List[str]]:
    """
    Check if required dependencies are installed.

    Returns:
        Tuple[bool, List[str]]: (all_installed, missing_packages)
    """
    required_packages = {
        "tensorflow": "TensorFlow",
        "numpy": "NumPy",
        "PIL": "Pillow",
        "cv2": "OpenCV",
        "matplotlib": "Matplotlib",
        "seaborn": "Seaborn",
        "sklearn": "Scikit-learn",
    }

    missing = []

    print("\nChecking dependencies...")
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing.append(package)

    return len(missing) == 0, missing


def check_gpu() -> bool:
    """
    Check if TensorFlow can access GPU.

    Returns:
        bool: True if GPU is available
    """
    try:
        import tensorflow as tf

        gpus = tf.config.list_physical_devices("GPU")

        if gpus:
            print(f"\n✅ GPU available: {len(gpus)} GPU(s) detected")
            for gpu in gpus:
                print(f"   - {gpu}")
            return True
        else:
            print("\n⚠️  No GPU detected. Training will use CPU (slower)")
            return False
    except Exception as e:
        print(f"\n⚠️  Could not check GPU: {str(e)}")
        return False


def check_dataset(dataset_dir: Path = Path("dataset")) -> bool:
    """
    Check if dataset is properly structured.

    Args:
        dataset_dir: Path to dataset directory

    Returns:
        bool: True if dataset is valid
    """
    print(f"\nChecking dataset at: {dataset_dir}")

    if not dataset_dir.exists():
        print(f"  ❌ Dataset directory not found: {dataset_dir}")
        print(f"   Please create a 'dataset' folder with class subdirectories")
        return False

    if not dataset_dir.is_dir():
        print(f"  ❌ Dataset path is not a directory: {dataset_dir}")
        return False

    # Count classes and images
    class_dirs = [d for d in dataset_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

    if not class_dirs:
        print(f"  ❌ No class directories found in {dataset_dir}")
        return False

    print(f"  ✅ Found {len(class_dirs)} classes")

    # Count images
    total_images = 0
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}

    for class_dir in class_dirs[:5]:  # Check first 5 classes
        images = []
        for ext in image_extensions:
            images.extend(class_dir.glob(f"*{ext}"))
            images.extend(class_dir.glob(f"*{ext.upper()}"))

        print(f"     - {class_dir.name}: {len(images)} images")
        total_images += len(images)

    if len(class_dirs) > 5:
        print(f"     ... and {len(class_dirs) - 5} more classes")

    if total_images == 0:
        print(f"  ❌ No images found in dataset")
        return False

    print(f"  ✅ Dataset structure is valid")
    return True


def check_directories() -> bool:
    """
    Check if required directories exist.

    Returns:
        bool: True if all directories are valid
    """
    print("\nChecking project directories...")

    required_dirs = [
        Path("dataset"),
        Path("models"),
        Path("output"),
        Path("output/plots"),
        Path("output/tensorboard"),
        Path("output/checkpoints"),
    ]

    all_valid = True

    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ⚠️  {dir_path} (will be created)")
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"     Created: {dir_path}")
            except Exception as e:
                print(f"     ❌ Could not create: {str(e)}")
                all_valid = False

    return all_valid


def print_system_info() -> None:
    """Print detailed system information."""
    import platform
    import psutil

    print("\n" + "=" * 60)
    print("System Information")
    print("=" * 60)
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Version: {sys.version}")

    # Memory info
    mem = psutil.virtual_memory()
    print(f"RAM: {mem.total / (1024**3):.2f} GB (Available: {mem.available / (1024**3):.2f} GB)")

    # Disk info
    disk = psutil.disk_usage("/")
    print(f"Disk: {disk.total / (1024**3):.2f} GB (Free: {disk.free / (1024**3):.2f} GB)")

    print("=" * 60)


def run_setup() -> bool:
    """
    Run complete setup check.

    Returns:
        bool: True if setup is complete
    """
    print("=" * 60)
    print("AgriGuard AI ML Pipeline - Setup Check")
    print("=" * 60)

    all_checks_passed = True

    # Check Python version
    if not check_python_version():
        all_checks_passed = False

    # Check dependencies
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        all_checks_passed = False
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install -r ml_pipeline/requirements.txt")

    # Check GPU
    check_gpu()

    # Check directories
    if not check_directories():
        all_checks_passed = False

    # Check dataset
    if not check_dataset():
        all_checks_passed = False
        print("\n⚠️  Dataset not found. Please prepare your dataset before training.")

    # Print system info
    print_system_info()

    # Final summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ Setup complete! You're ready to train the model.")
        print("\nNext steps:")
        print("  1. python ml_pipeline/train.py")
        print("  2. python ml_pipeline/predict.py <image_path>")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
    print("=" * 60)

    return all_checks_passed


def create_sample_dataset_structure() -> None:
    """Create sample dataset directory structure."""
    sample_classes = [
        "Tomato___Healthy",
        "Tomato___Late_Blight",
        "Tomato___Early_Blight",
        "Corn___Healthy",
        "Corn___Common_Rust",
        "Corn___Northern_Leaf_Blight",
        "Potato___Healthy",
        "Potato___Late_Blight",
        "Rice___Blast",
        "Rice___Brown_Spot",
        "Wheat___Rust",
        "Wheat___Healthy",
    ]

    dataset_dir = Path("dataset")

    print("\nCreating sample dataset structure...")
    for class_name in sample_classes:
        class_dir = dataset_dir / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {class_dir}")

    print(f"\n✅ Sample dataset structure created at: {dataset_dir}")
    print("   Add your images to the respective class folders.")


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="AgriGuard AI ML Pipeline Setup")
    parser.add_argument(
        "--create-sample-dataset",
        action="store_true",
        help="Create sample dataset directory structure",
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Run checks without creating directories"
    )

    args = parser.parse_args()

    if args.create_sample_dataset:
        create_sample_dataset_structure()
    else:
        run_setup()


if __name__ == "__main__":
    main()
