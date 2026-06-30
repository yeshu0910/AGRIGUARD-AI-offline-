# AgriGuard AI ML Pipeline

A production-ready, offline crop disease detection system using TensorFlow/Keras and EfficientNetB0 for transfer learning.

## Features

- **Offline-First**: Complete inference without internet connectivity
- **Transfer Learning**: EfficientNetB0 with ImageNet pretrained weights
- **Automatic Class Detection**: Discovers classes from dataset directory structure
- **Two-Phase Training**: Initial training + fine-tuning for optimal performance
- **Comprehensive Evaluation**: Confusion matrix, classification report, ROC curves
- **Model Explainability**: Grad-CAM and saliency map visualizations
- **Batch Prediction**: Support for multiple images
- **Confidence Thresholding**: Handles unknown crops/diseases gracefully
- **Streamlit Integration**: Ready-to-use prediction module

## Project Structure

```
ml_pipeline/
├── __init__.py           # Package initialization
├── config.py             # Configuration management
├── utils.py              # Utility functions
├── dataset_loader.py     # Dataset loading and preprocessing
├── model.py              # Model architecture (EfficientNetB0)
├── train.py              # Training pipeline
├── predict.py            # Prediction and inference
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.10+
- TensorFlow 2.15+
- 8GB+ RAM recommended
- GPU optional (CPU-only supported)

### Install Dependencies

```bash
# Install ML pipeline dependencies
pip install -r ml_pipeline/requirements.txt

# Or install individually
pip install tensorflow>=2.15.0 numpy>=1.26.0 Pillow>=10.0.0
pip install matplotlib>=3.8.0 seaborn>=0.13.0 scikit-learn>=1.4.0
```

## Quick Start

### 1. Prepare Dataset

Organize your dataset in the following structure:

```
dataset/
├── Tomato___Healthy/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Tomato___Late_Blight/
│   ├── image1.jpg
│   └── ...
├── Corn___Healthy/
│   └── ...
└── ...
```

**Requirements:**
- Each subdirectory represents one class
- Directory name format: `Crop___Disease` or `Crop___Healthy`
- Supported image formats: JPG, JPEG, PNG, BMP, TIFF
- Images can be of leaves, fruits, stems, flowers, or roots

### 2. Train Model

```bash
# Basic training
python ml_pipeline/train.py

# With custom dataset directory
python ml_pipeline/train.py --dataset-dir /path/to/dataset

# Custom epochs
python ml_pipeline/train.py --epochs-initial 30 --epochs-fine-tune 15
```

**Training Process:**
1. Validates dataset structure
2. Automatically discovers classes
3. Saves classes to `models/classes.json`
4. Creates train/validation split (80/20)
5. Phase 1: Trains classification head (20 epochs)
6. Phase 2: Fine-tunes EfficientNetB0 (10 epochs)
7. Evaluates model and generates metrics
8. Saves model to `models/agriguard_model.keras`

### 3. Make Predictions

```python
from ml_pipeline import create_predictor
from PIL import Image

# Create predictor
predictor = create_predictor()

# Load and predict
image = Image.open("test_image.jpg")
result = predictor.predict(image)

# Access results
print(f"Crop: {result['crop']}")
print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Severity: {result['severity']}")
print(f"Recommendations: {result['recommendations']}")
```

### 4. Command-Line Prediction

```bash
# Basic prediction
python ml_pipeline/predict.py test_image.jpg

# With Grad-CAM visualization
python ml_pipeline/predict.py test_image.jpg --gradcam --output gradcam.png

# Custom model path
python ml_pipeline/predict.py test_image.jpg --model /path/to/model.keras
```

## Configuration

Edit `ml_pipeline/config.py` to customize:

### Model Configuration
```python
IMG_SIZE = 224              # Input image size
BASE_MODEL = "EfficientNetB0"
WEIGHTS = "imagenet"        # Pretrained weights
FREEZE_BASE = True          # Freeze base model initially
UNFREEZE_LAYERS = 100       # Layers to unfreeze for fine-tuning
```

### Training Configuration
```python
TRAIN_SPLIT = 0.8          # Training set ratio
BATCH_SIZE = 32             # Batch size
INITIAL_EPOCHS = 20         # Initial training epochs
FINE_TUNE_EPOCHS = 10       # Fine-tuning epochs
LEARNING_RATE = 0.001       # Initial learning rate
FINE_TUNE_LR = 0.0001       # Fine-tuning learning rate
```

### Augmentation Configuration
```python
RANDOM_FLIP = "horizontal"  # Flip mode: "horizontal", "vertical", or None
RANDOM_ROTATION = 0.2       # Rotation range (20%)
RANDOM_ZOOM = 0.2           # Zoom range (20%)
RANDOM_CONTRAST = 0.2       # Contrast range (20%)
RANDOM_BRIGHTNESS = 0.2     # Brightness range (20%)
```

### Prediction Configuration
```python
CONFIDENCE_THRESHOLD = 0.70  # Minimum confidence (70%)
TOP_K_PREDICTIONS = 5        # Number of top predictions
GENERATE_GRADCAM = True      # Enable Grad-CAM
GENERATE_SALIENCY = False    # Enable saliency maps
```

## Output Files

After training, the following files are generated:

```
models/
├── agriguard_model.keras    # Trained model
└── classes.json             # Class names and metadata

output/
├── training_history.json    # Training metrics history
├── training_metrics.json    # Final evaluation metrics
├── model_info.json          # Model architecture info
├── plots/
│   ├── training_history.png
│   ├── confusion_matrix.png
│   └── classification_report.png
├── tensorboard/             # TensorBoard logs
└── checkpoints/
    └── best_model.keras     # Best checkpoint
```

## Metrics Generated

### Overall Metrics
- Loss
- Accuracy
- Top-5 Accuracy
- Precision (macro & weighted)
- Recall (macro & weighted)
- F1 Score (macro & weighted)
- AUC

### Per-Class Metrics
- Precision
- Recall
- F1 Score
- Support (sample count)

### Visualizations
- Training/validation accuracy and loss curves
- Confusion matrix (counts and normalized)
- Classification report heatmap

## Streamlit Integration

### Basic Integration

```python
import streamlit as st
from ml_pipeline import create_predictor, format_prediction_for_streamlit

# Load model (cache for performance)
@st.cache_resource
def load_model():
    return create_predictor()

predictor = load_model()

# Upload image
uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    
    # Predict
    result = predictor.predict(image)
    formatted = format_prediction_for_streamlit(result)
    
    # Display results
    st.header("Prediction Results")
    st.write(f"**Crop:** {formatted['crop']}")
    st.write(f"**Disease:** {formatted['disease']}")
    st.write(f"**Confidence:** {formatted['confidence']}")
    st.write(f"**Severity:** {formatted['severity']}")
    st.write(f"**Prediction Time:** {formatted['prediction_time']}")
    
    # Top 5 predictions
    st.subheader("Top 5 Predictions")
    for pred in formatted['top_5']:
        st.write(f"{pred['crop']} - {pred['disease']}: {pred['confidence']:.2%}")
    
    # Recommendations
    st.subheader("Recommendations")
    for rec in formatted['recommendations']:
        st.write(f"• {rec}")
    
    # Grad-CAM visualization
    if st.checkbox("Show Grad-CAM"):
        gradcam = predictor.generate_gradcam(image)
        st.image(gradcam, caption="Grad-CAM Visualization")
```

### Advanced Streamlit App

See `streamlit_app.py` example in the main project directory.

## Model Architecture

```
Input (224x224x3)
    ↓
EfficientNetB0 (pretrained, frozen initially)
    ↓
Global Average Pooling
    ↓
Dropout (0.3)
    ↓
Dense (512, ReLU)
Batch Normalization
Dropout (0.4)
    ↓
Dense (256, ReLU)
Batch Normalization
Dropout (0.3)
    ↓
Dense (N, Softmax)  # N = number of classes
```

## Supported Crops

The system automatically supports any crop present in your dataset. Example crops:

- Tomato
- Potato
- Maize (Corn)
- Rice
- Wheat
- Cotton
- Soybean
- Pepper
- Apple
- Grape
- Banana
- Mango

**Adding new crops:** Simply add new folders to the `dataset/` directory with the format `Crop___Disease`. The system will automatically detect and train on them.

## Supported Plant Parts

The model learns from images of:
- Leaves
- Fruits
- Stems
- Flowers
- Roots
- Corn ears/cobs

**Note:** Avoid restricting training to only leaf images for better generalization.

## Advanced Features

### Batch Prediction

```python
from ml_pipeline import create_predictor
from pathlib import Path

predictor = create_predictor()

# Predict on multiple images
image_paths = list(Path("test_images/").glob("*.jpg"))
results = predictor.predict_batch(image_paths)

for result in results:
    print(f"{result['crop']} - {result['disease']}: {result['confidence']:.2%}")
```

### Grad-CAM Visualization

```python
from ml_pipeline import create_predictor
from PIL import Image

predictor = create_predictor()
image = Image.open("test_image.jpg")

# Generate Grad-CAM
gradcam = predictor.generate_gradcam(image)
gradcam.save("gradcam_output.png")
```

### Saliency Maps

```python
# Generate saliency map
saliency = predictor.generate_saliency_map(image)
saliency.save("saliency_output.png")
```

### Model Export (ONNX)

```python
# Convert to ONNX (requires onnx-tf)
import tf2onnx

model = predictor.model
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=[...])
onnx_model.save("model.onnx")
```

### TensorFlow Lite Export

```python
# Convert to TFLite for mobile deployment
converter = tf.lite.TFLiteConverter.from_keras_model(predictor.model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)
```

## Performance Optimization

### Training
- Use mixed precision training (if GPU available)
- Adjust batch size based on available memory
- Use data caching for faster epoch loading
- Enable prefetching: `dataset = dataset.prefetch(tf.data.AUTOTUNE)`

### Inference
- Cache model in memory (use `@st.cache_resource` in Streamlit)
- Batch predictions when processing multiple images
- Use TensorFlow Lite for edge deployment
- Quantize model for faster inference

## Troubleshooting

### Out of Memory (OOM)
- Reduce `BATCH_SIZE` in config
- Reduce `IMG_SIZE` (e.g., 192x192 instead of 224x224)
- Use gradient checkpointing
- Enable mixed precision

### Poor Accuracy
- Increase training data
- Add more augmentation
- Train for more epochs
- Adjust learning rate
- Use class weights for imbalanced datasets

### Slow Training
- Reduce model size (use EfficientNetB1-B7)
- Use smaller input size
- Disable TensorBoard logging
- Use fewer augmentation operations

## Best Practices

1. **Dataset Quality**: Use high-quality, diverse images
2. **Class Balance**: Ensure roughly equal samples per class
3. **Data Augmentation**: Use appropriate augmentation for your use case
4. **Validation**: Always keep a separate validation set
5. **Monitoring**: Use TensorBoard to monitor training
6. **Checkpoints**: Save best models with ModelCheckpoint
7. **Testing**: Test on real-world images before deployment

## API Reference

### DatasetLoader

```python
from ml_pipeline import DatasetLoader

loader = DatasetLoader(dataset_dir=Path("./dataset"))
classes = loader.discover_classes()
train_gen, val_gen = loader.load_dataset()
```

### CropDiseaseModel

```python
from ml_pipeline import create_model

model = create_model(num_classes=38)
model.train(train_gen, val_gen)
model.save_model()
```

### CropDiseasePredictor

```python
from ml_pipeline import create_predictor

predictor = create_predictor()
result = predictor.predict(image)
gradcam = predictor.generate_gradcam(image)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in `docs/`
- Review example notebooks

## Citation

If you use this project in your research, please cite:

```bibtex
@software{agriguard_ai_2024,
  title = {AgriGuard AI: Offline Crop Disease Detection},
  year = {2024},
  url = {https://github.com/your-repo/agriguard-ai}
}
```

## Acknowledgments

- TensorFlow Team for EfficientNet implementation
- PlantVillage dataset for inspiration
- Agricultural research community

---

**Built with ❤️ for sustainable agriculture**