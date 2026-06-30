# AgriGuard AI - ML Pipeline Documentation

## 🎯 Overview

The AgriGuard AI ML Pipeline is a **production-ready, offline crop disease detection system** built with TensorFlow/Keras and EfficientNetB0. It enables automatic identification of multiple crops and their diseases from images without requiring internet connectivity.

## ✨ Key Features

### 🤖 Deep Learning
- **EfficientNetB0** with ImageNet pretrained weights
- **Transfer Learning** for optimal performance
- **Two-phase training**: Classification head + fine-tuning
- **Automatic class detection** from dataset structure

### 📊 Comprehensive Evaluation
- Training/validation accuracy and loss curves
- Confusion matrix (counts and normalized)
- Classification report with per-class metrics
- Top-5 accuracy, precision, recall, F1-score, AUC
- TensorBoard integration for real-time monitoring

### 🔍 Model Explainability
- **Grad-CAM** visualizations showing model attention
- **Saliency maps** for feature importance
- Confidence scoring with severity levels

### 🎨 Data Augmentation
- Random flip (horizontal/vertical)
- Random rotation (±20%)
- Random zoom (±20%)
- Random contrast (±20%)
- Random brightness (±20%)

### 🌾 Supported Crops
Automatically supports any crop in your dataset:
- Tomato, Potato, Maize (Corn), Rice, Wheat
- Cotton, Soybean, Pepper, Apple, Grape
- Banana, Mango, and more...

### 🍃 Supported Plant Parts
- Leaves, Fruits, Stems, Flowers, Roots
- Corn ears/cobs
- Any plant part with visible disease symptoms

### 💻 Offline-First Design
- No internet required for inference
- No cloud APIs
- No remote model downloads
- Everything runs locally

## 📁 Project Structure

```
agriguard-ai/
├── ml_pipeline/                    # ML Pipeline Package
│   ├── __init__.py                # Package initialization
│   ├── config.py                  # Configuration management
│   ├── utils.py                   # Utility functions
│   ├── dataset_loader.py          # Dataset loading & preprocessing
│   ├── model.py                   # EfficientNetB0 model architecture
│   ├── train.py                   # Training pipeline
│   ├── predict.py                 # Prediction & inference
│   ├── streamlit_app.py           # Streamlit web interface
│   ├── setup.py                   # Setup & validation script
│   ├── requirements.txt           # Python dependencies
│   ├── .gitignore                 # Git ignore rules
│   ├── README.md                  # Detailed documentation
│   ├── GETTING_STARTED.md         # Quick start guide
│   └── examples/
│       ├── __init__.py
│       └── basic_usage.py         # Usage examples
├── dataset/                       # Your dataset (gitignored)
│   ├── Tomato___Healthy/
│   ├── Tomato___Late_Blight/
│   └── ...
├── models/                        # Trained models (gitignored)
│   ├── agriguard_model.keras
│   └── classes.json
├── output/                        # Training outputs (gitignored)
│   ├── training_history.json
│   ├── training_metrics.json
│   ├── plots/
│   ├── tensorboard/
│   └── checkpoints/
├── backend/                       # FastAPI backend
├── frontend/                      # HTML5 frontend
├── docs/                          # Documentation
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r ml_pipeline/requirements.txt

# Or install individually
pip install tensorflow>=2.15.0 numpy>=1.26.0 Pillow>=10.0.0
pip install matplotlib>=3.8.0 seaborn>=0.13.0 scikit-learn>=1.4.0
```

### 2. Prepare Dataset

Organize images in this structure:
```
dataset/
├── Tomato___Healthy/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
├── Tomato___Late_Blight/
│   └── ...
└── ...
```

**Format:** `Crop___Disease` or `Crop___Healthy`

### 3. Verify Setup

```bash
python ml_pipeline/setup.py
```

### 4. Train Model

```bash
python ml_pipeline/train.py
```

**Training Process:**
- Phase 1: Train classification head (20 epochs)
- Phase 2: Fine-tune EfficientNetB0 (10 epochs)
- Total time: 2-6 hours (CPU) or 30 min - 2 hours (GPU)

### 5. Make Predictions

```bash
# Command line
python ml_pipeline/predict.py test_image.jpg

# With Grad-CAM
python ml_pipeline/predict.py test_image.jpg --gradcam --output viz.png
```

### 6. Launch Web App

```bash
streamlit run ml_pipeline/streamlit_app.py
```

## 📖 Documentation

### Core Documentation
- **[GETTING_STARTED.md](ML_PIPELINE_GETTING_STARTED.md)** - Step-by-step tutorial
- **[ml_pipeline/README.md](ml_pipeline/README.md)** - Complete API reference
- **[ml_pipeline/GETTING_STARTED.md](ml_pipeline/GETTING_STARTED.md)** - Detailed getting started guide

### Key Files
- **config.py** - All configuration parameters
- **train.py** - Training pipeline orchestration
- **predict.py** - Inference and prediction logic
- **streamlit_app.py** - Web interface

## 🔧 Configuration

Edit `ml_pipeline/config.py` to customize:

```python
# Model
IMG_SIZE = 224
BASE_MODEL = "EfficientNetB0"
UNFREEZE_LAYERS = 100

# Training
BATCH_SIZE = 32
INITIAL_EPOCHS = 20
FINE_TUNE_EPOCHS = 10
LEARNING_RATE = 0.001

# Augmentation
RANDOM_FLIP = "horizontal"
RANDOM_ROTATION = 0.2
RANDOM_ZOOM = 0.2

# Prediction
CONFIDENCE_THRESHOLD = 0.70
TOP_K_PREDICTIONS = 5
```

## 💻 Usage Examples

### Python API

```python
from ml_pipeline import create_predictor, DatasetLoader
from PIL import Image

# Training
loader = DatasetLoader()
classes = loader.discover_classes()
train_gen, val_gen = loader.load_dataset()

from ml_pipeline import create_model
model = create_model(num_classes=len(classes))
model.train(train_gen, val_gen)
model.save_model()

# Prediction
predictor = create_predictor()
image = Image.open("test.jpg")
result = predictor.predict(image)

print(f"Crop: {result['crop']}")
print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Recommendations: {result['recommendations']}")
```

### Streamlit Integration

```python
import streamlit as st
from ml_pipeline import create_predictor

@st.cache_resource
def load_model():
    return create_predictor()

predictor = load_model()
uploaded_file = st.file_uploader("Upload image")

if uploaded_file:
    image = Image.open(uploaded_file)
    result = predictor.predict(image)
    
    st.write(f"**Crop:** {result['crop']}")
    st.write(f"**Disease:** {result['disease']}")
    st.write(f"**Confidence:** {result['confidence']:.2%}")
```

### Batch Prediction

```python
from pathlib import Path

predictor = create_predictor()
image_paths = list(Path("test_images/").glob("*.jpg"))
results = predictor.predict_batch(image_paths)

for result in results:
    print(f"{result['crop']} - {result['disease']}")
```

## 📊 Output Files

After training, you'll have:

```
models/
├── agriguard_model.keras    # Trained model
└── classes.json             # Class names

output/
├── training_history.json    # Training metrics
├── training_metrics.json    # Evaluation metrics
├── model_info.json          # Model architecture
├── plots/
│   ├── training_history.png
│   ├── confusion_matrix.png
│   └── classification_report.png
├── tensorboard/             # TensorBoard logs
└── checkpoints/
    └── best_model.keras     # Best checkpoint
```

## 🎯 Model Architecture

```
Input (224x224x3)
    ↓
EfficientNetB0 (pretrained, frozen)
    ↓
Global Average Pooling
    ↓
Dropout (0.3)
    ↓
Dense (512, ReLU) + BatchNorm + Dropout (0.4)
    ↓
Dense (256, ReLU) + BatchNorm + Dropout (0.3)
    ↓
Dense (N, Softmax)  # N = number of classes
```

**Total Parameters:** ~5.3M (EfficientNetB0 base + classification head)

## 📈 Performance Metrics

The system generates comprehensive metrics:

### Overall Metrics
- **Accuracy**: Overall prediction accuracy
- **Top-5 Accuracy**: Correct class in top 5 predictions
- **Precision**: True positive rate
- **Recall**: Coverage of actual positives
- **F1 Score**: Balance of precision and recall
- **AUC**: Model discrimination ability

### Per-Class Metrics
- Precision, Recall, F1-Score for each class
- Support (number of samples)

### Visualizations
- Training/validation curves
- Confusion matrix
- Classification report heatmap

## 🔒 Offline Requirements

✅ **No internet required** after initial setup
✅ **No cloud APIs** - all inference is local
✅ **No online model downloads** - model saved locally
✅ **No remote database** - SQLite for metadata
✅ **CPU-only inference** - no GPU required for prediction

## 🛠️ Advanced Features

### Grad-CAM Visualization

```python
gradcam = predictor.generate_gradcam(image)
gradcam.save("gradcam.png")
```

### Model Export

```python
# TensorFlow Lite for mobile
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# ONNX for cross-platform
import tf2onnx
onnx_model, _ = tf2onnx.convert.from_keras(model)
```

### Custom Configuration

```python
from ml_pipeline.config import update_config

update_config(
    training__BATCH_SIZE=16,
    training__LEARNING_RATE=0.0005,
    prediction__CONFIDENCE_THRESHOLD=0.80
)
```

## 🧪 Testing

```bash
# Run setup check
python ml_pipeline/setup.py

# Test imports
python -c "from ml_pipeline import create_predictor; print('OK')"

# Run examples
python ml_pipeline/examples/basic_usage.py
```

## 📚 Dataset Sources

### Recommended Datasets

1. **PlantVillage Dataset** (Recommended)
   - URL: https://data.mendeley.com/datasets/tywbtsjrjv/1
   - 54,000+ images
   - 38 classes
   - Multiple crops and diseases

2. **PlantDoc Dataset**
   - Real-world images
   - More diverse backgrounds

3. **Custom Dataset**
   - Collect your own images
   - Minimum 50 images per class
   - More is better (100+ recommended)

### Dataset Best Practices

✅ **Do:**
- Use high-quality, clear images
- Include diverse lighting conditions
- Capture multiple angles
- Balance classes (equal samples)
- Include healthy and diseased samples

❌ **Don't:**
- Use blurry or dark images
- Mix different plant species
- Have highly imbalanced classes
- Use only one type of image (e.g., only leaves)

## 🚀 Deployment

### Local Deployment
```bash
# Train once, predict many times
python ml_pipeline/train.py
python ml_pipeline/predict.py image.jpg
```

### Web Application
```bash
streamlit run ml_pipeline/streamlit_app.py
```

### API Integration
```python
# Integrate with existing FastAPI backend
from ml_pipeline import create_predictor

predictor = create_predictor()

@app.post("/predict")
async def predict(file: UploadFile):
    image = Image.open(file.file)
    result = predictor.predict(image)
    return result
```

### Mobile Deployment
```python
# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

## 🤝 Integration with Existing Project

### Backend Integration

The ML pipeline integrates seamlessly with the existing FastAPI backend:

```python
# backend/routers/prediction.py
from ml_pipeline import create_predictor

predictor = create_predictor()

@router.post("/predict")
async def predict_disease(file: UploadFile):
    image = Image.open(file.file)
    result = predictor.predict(image)
    return result
```

### Frontend Integration

Use the prediction API from the HTML5 frontend:

```javascript
// Upload image and get prediction
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('/api/predict', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result.crop, result.disease);
```

## 📝 Code Quality

### Standards Followed
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ Modular architecture
- ✅ Logging throughout
- ✅ Exception handling
- ✅ Configuration management
- ✅ No hardcoded paths
- ✅ Cross-platform support

### Best Practices
- Separation of concerns
- Single responsibility principle
- DRY (Don't Repeat Yourself)
- Clean, readable code
- Extensive comments
- Production-ready error handling

## 🐛 Troubleshooting

### Common Issues

**Issue: Out of Memory**
```python
# Reduce batch size in config.py
BATCH_SIZE = 16  # Instead of 32
```

**Issue: Poor Accuracy**
- Add more training data
- Increase augmentation
- Train longer (more epochs)
- Balance classes

**Issue: Slow Training**
- Use GPU
- Reduce image size
- Disable TensorBoard

**Issue: Module Not Found**
```bash
pip install -r ml_pipeline/requirements.txt
```

## 📊 Performance Benchmarks

### Expected Performance (PlantVillage Dataset)

| Metric | Target | Excellent |
|--------|--------|-----------|
| Accuracy | > 85% | > 95% |
| Top-5 Accuracy | > 95% | > 99% |
| F1 Score | > 0.80 | > 0.95 |
| Inference Time | < 0.5s | < 0.1s |

### Training Time

| Setup | Dataset Size | Time |
|-------|-------------|------|
| CPU (8GB RAM) | 10,000 images | 4-6 hours |
| CPU (16GB RAM) | 10,000 images | 2-3 hours |
| GPU (GTX 1060) | 10,000 images | 30-60 min |
| GPU (RTX 3080) | 10,000 images | 15-30 min |

## 🎓 Learning Resources

### Understanding the Code

1. **Start Here**: `GETTING_STARTED.md`
2. **Configuration**: `config.py`
3. **Data Flow**: `dataset_loader.py`
4. **Model**: `model.py`
5. **Training**: `train.py`
6. **Inference**: `predict.py`

### Key Concepts

- **Transfer Learning**: Using pretrained models
- **Fine-tuning**: Adapting pretrained models to new tasks
- **Data Augmentation**: Artificially expanding training data
- **EfficientNet**: State-of-the-art CNN architecture
- **Grad-CAM**: Model interpretability technique

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes and test
4. Submit pull request

## 📄 License

MIT License - See LICENSE file

## 👥 Authors

AgriGuard AI Team

## 🙏 Acknowledgments

- TensorFlow Team for EfficientNet
- PlantVillage dataset contributors
- Agricultural research community

---

## 📞 Support

- **Documentation**: Check `ml_pipeline/README.md`
- **Issues**: Open GitHub issue
- **Examples**: See `ml_pipeline/examples/`

---

**Built with ❤️ for sustainable agriculture and food security**

🌱 AgriGuard AI - Protecting crops, feeding the world 🌱