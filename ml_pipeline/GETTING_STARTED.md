# Getting Started with AgriGuard AI ML Pipeline

This guide will help you get up and running with the crop disease detection system in 5 simple steps.

## Prerequisites

Before you begin, ensure you have:
- Python 3.10 or higher
- 8GB+ RAM (16GB recommended)
- 10GB+ free disk space
- (Optional) GPU for faster training

## Step 1: Install Dependencies

```bash
# Navigate to project directory
cd agriguard-ai

# Install ML pipeline dependencies
pip install -r ml_pipeline/requirements.txt
```

**Expected time:** 5-10 minutes

## Step 2: Prepare Your Dataset

### Option A: Use PlantVillage Dataset (Recommended for Testing)

1. Download the [PlantVillage Dataset](https://data.mendeley.com/datasets/tywbtsjrjv/1)
2. Extract the dataset
3. Organize it in the required structure:

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

**Naming Convention:**
- Format: `Crop___Disease` or `Crop___Healthy`
- Examples: `Tomato___Late_Blight`, `Potato___Healthy`, `Rice___Blast`
- Use underscores instead of spaces

### Option B: Create Your Own Dataset

1. Collect images of crops with diseases
2. Organize by crop and disease type
3. Ensure each class has 50+ images (more is better)
4. Use diverse images (different lighting, angles, backgrounds)

**Image Requirements:**
- Formats: JPG, JPEG, PNG, BMP, TIFF
- Resolution: At least 224x224 pixels
- Content: Clear images of affected plant parts (leaves, fruits, stems, etc.)

### Option C: Create Sample Structure

```bash
# Create sample directory structure
python ml_pipeline/setup.py --create-sample-dataset
```

## Step 3: Verify Setup

Run the setup checker to ensure everything is configured correctly:

```bash
python ml_pipeline/setup.py
```

**Expected output:**
```
✅ Python 3.x.x (>= 3.10)
✅ TensorFlow
✅ NumPy
✅ Pillow
✅ Matplotlib
✅ Seaborn
✅ Scikit-learn
✅ Found X classes
✅ Dataset structure is valid
✅ Setup complete! You're ready to train the model.
```

## Step 4: Train the Model

### Basic Training

```bash
python ml_pipeline/train.py
```

**What happens:**
1. Validates dataset structure
2. Discovers all classes automatically
3. Saves classes to `models/classes.json`
4. Splits data: 80% training, 20% validation
5. Phase 1: Trains classification head (20 epochs)
6. Phase 2: Fine-tunes EfficientNetB0 (10 epochs)
7. Evaluates model and generates metrics
8. Saves model to `models/agriguard_model.keras`

**Expected time:**
- CPU only: 2-6 hours (depends on dataset size)
- GPU: 30 minutes - 2 hours

### Advanced Training Options

```bash
# Custom dataset directory
python ml_pipeline/train.py --dataset-dir /path/to/your/dataset

# Custom epochs
python ml_pipeline/train.py --epochs-initial 30 --epochs-fine-tune 15

# Combine options
python ml_pipeline/train.py --dataset-dir ./my_dataset --epochs-initial 25 --epochs-fine-tune 12
```

### Monitor Training

**TensorBoard:**
```bash
tensorboard --logdir output/tensorboard
```
Then open http://localhost:6006 in your browser.

**Check progress:**
- Training logs are saved to `agriguard.log`
- Checkpoints are saved to `output/checkpoints/`
- Plots are saved to `output/plots/`

## Step 5: Make Predictions

### Command-Line Prediction

```bash
# Basic prediction
python ml_pipeline/predict.py test_image.jpg

# With Grad-CAM visualization
python ml_pipeline/predict.py test_image.jpg --gradcam --output visualization.png

# Custom model path
python ml_pipeline/predict.py test_image.jpg --model /path/to/model.keras
```

**Example output:**
```
============================================================
Prediction Results
============================================================
Crop: Tomato
Disease: Late Blight
Confidence: 94.52%
Severity: High
Prediction Time: 0.123s

Top 5 Predictions:
  1. Tomato - Late Blight: 94.52%
  2. Tomato - Early Blight: 3.21%
  3. Tomato - Healthy: 1.15%
  4. Potato - Late Blight: 0.78%
  5. Corn - Common Rust: 0.34%

Recommendations:
  • Apply copper-based fungicides as preventive measure
  • Remove and destroy infected plant parts
  • Improve drainage in the field
  • Consult with local agricultural extension officer
============================================================
```

### Python API

```python
from ml_pipeline import create_predictor
from PIL import Image

# Load predictor
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

# Generate Grad-CAM
gradcam = predictor.generate_gradcam(image)
gradcam.save("gradcam.png")
```

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

## Step 6: Launch Streamlit App (Optional)

```bash
streamlit run ml_pipeline/streamlit_app.py
```

The web interface will open at http://localhost:8501

**Features:**
- Drag-and-drop image upload
- Real-time predictions
- Grad-CAM visualization
- Confidence scoring
- Treatment recommendations
- Model information display

## Understanding the Output

### Model Files

After training, you'll find:

```
models/
├── agriguard_model.keras    # Trained model (100-500MB)
└── classes.json             # Class names and metadata

output/
├── training_history.json    # Training metrics
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

### Metrics Explained

**Overall Metrics:**
- **Accuracy**: Percentage of correct predictions
- **Top-5 Accuracy**: Correct class in top 5 predictions
- **Precision**: True positives / (True + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall
- **AUC**: Area under ROC curve

**Good Performance Indicators:**
- Accuracy > 85%
- F1 Score > 0.80
- Low validation loss

## Troubleshooting

### Issue: "Dataset directory not found"

**Solution:**
```bash
# Create dataset directory
mkdir dataset

# Organize your images in subdirectories
# Format: dataset/Crop___Disease/image.jpg
```

### Issue: "Out of Memory (OOM)"

**Solutions:**
1. Reduce batch size in `config.py`:
   ```python
   BATCH_SIZE = 16  # Instead of 32
   ```

2. Reduce image size:
   ```python
   IMG_SIZE = 192  # Instead of 224
   ```

3. Close other applications

### Issue: "Poor accuracy (< 70%)"

**Solutions:**
1. **More data**: Add more images per class (aim for 100+)
2. **Better quality**: Use clear, well-lit images
3. **More augmentation**: Increase augmentation in config
4. **Longer training**: Increase epochs
5. **Class balance**: Ensure equal samples per class

### Issue: "Training is very slow"

**Solutions:**
1. Use GPU if available
2. Reduce model size (use EfficientNetB1-B7)
3. Reduce image size
4. Disable TensorBoard: Set `histogram_freq=0`
5. Use fewer augmentation operations

### Issue: "Module not found errors"

**Solution:**
```bash
# Ensure you're in the correct directory
cd agriguard-ai

# Install dependencies
pip install -r ml_pipeline/requirements.txt

# Verify installation
python -c "import ml_pipeline; print('OK')"
```

## Next Steps

### 1. Improve Your Model

- Collect more diverse images
- Try different augmentation strategies
- Experiment with learning rates
- Use class weights for imbalanced datasets

### 2. Deploy the Model

**TensorFlow Lite (Mobile):**
```python
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)
```

**ONNX (Cross-platform):**
```python
import tf2onnx

onnx_model, _ = tf2onnx.convert.from_keras(model)
onnx_model.save("model.onnx")
```

### 3. Integrate with Backend

See the existing FastAPI backend in `backend/` for API integration.

### 4. Expand the System

- Add more crops and diseases
- Implement ensemble models
- Add disease severity estimation
- Integrate weather data
- Build mobile app

## Resources

- **Documentation**: See `ml_pipeline/README.md` for detailed docs
- **Examples**: Check `ml_pipeline/examples/` for code examples
- **Dataset**: [PlantVillage](https://data.mendeley.com/datasets/tywbtsjrjv/1)
- **TensorFlow Docs**: https://www.tensorflow.org/api_docs

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review the logs in `agriguard.log`
3. Ensure dataset is properly formatted
4. Open an issue on GitHub

## Quick Reference

| Task | Command |
|------|---------|
| Setup check | `python ml_pipeline/setup.py` |
| Train model | `python ml_pipeline/train.py` |
| Predict | `python ml_pipeline/predict.py image.jpg` |
| Grad-CAM | `python ml_pipeline/predict.py image.jpg --gradcam` |
| Streamlit app | `streamlit run ml_pipeline/streamlit_app.py` |
| TensorBoard | `tensorboard --logdir output/tensorboard` |

---

**Ready to start?** Begin with Step 1 and work your way through. Happy training! 🌿