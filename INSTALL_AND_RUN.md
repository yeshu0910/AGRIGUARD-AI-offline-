# Installation and Running Guide

## Quick Installation

The test output shows that dependencies need to be installed. This is expected! Follow these steps:

### Step 1: Install Dependencies

```bash
# From the project root directory
pip install -r ml_pipeline/requirements.txt
```

**This will install:**
- TensorFlow 2.15+ (for deep learning)
- NumPy (for numerical operations)
- Pillow (for image processing)
- Matplotlib & Seaborn (for plotting)
- Scikit-learn (for metrics)
- Streamlit (for web interface)

**Installation time:** 5-10 minutes

### Step 2: Verify Installation

```bash
# Run the test suite
python ml_pipeline/test_pipeline.py
```

**Expected output after installation:**
```
============================================================
AgriGuard AI ML Pipeline - Test Suite
============================================================
Testing imports...
  ✅ TensorFlow 2.15.0
  ✅ NumPy 1.26.0
  ✅ Pillow
  ✅ Matplotlib
  ✅ Seaborn
  ✅ Scikit-learn

Testing ml_pipeline modules...
  ✅ ml_pipeline.config
  ✅ ml_pipeline.utils
  ✅ ml_pipeline.dataset_loader
  ✅ ml_pipeline.model
  ✅ ml_pipeline.predict

Testing configuration...
  ✅ Configuration valid

Testing utilities...
  ✅ parse_class_name works
  ✅ format_class_name works
  ✅ get_severity works
  ✅ get_recommendations works
  ✅ Timer works

Testing model architecture...
  ✅ Model architecture works
     - Parameters: 5,300,000
     - Input shape: (224, 224, 3)
     - Output shape: (1, 5)

Testing dataset loader...
  ✅ DatasetLoader initializes correctly

Testing predictor...
  ✅ CropDiseasePredictor initializes correctly

============================================================
Test Summary
============================================================
✅ Imports: Passed
✅ Configuration: Configuration test passed
✅ Utilities: Utility tests passed
✅ Model Architecture: Model architecture test passed
✅ Dataset Loader: Dataset loader test passed
✅ Predictor: Predictor test passed
============================================================
Results: 6/6 tests passed
✅ All tests passed! Pipeline is ready.
```

## Complete Setup Workflow

### 1. Install Dependencies (One-time)

```bash
# Windows
pip install -r ml_pipeline/requirements.txt

# Or with pip3
pip3 install -r ml_pipeline/requirements.txt

# Or install individually if needed
pip install tensorflow>=2.15.0
pip install numpy>=1.26.0
pip install Pillow>=10.0.0
pip install matplotlib>=3.8.0
pip install seaborn>=0.13.0
pip install scikit-learn>=1.4.0
pip install streamlit
```

### 2. Prepare Dataset

**Option A: Use PlantVillage Dataset**
```bash
# Download from: https://data.mendeley.com/datasets/tywbtsjrjv/1
# Extract and organize as:
# dataset/
#   Tomato___Healthy/
#   Tomato___Late_Blight/
#   Corn___Healthy/
#   ...
```

**Option B: Create Sample Structure**
```bash
python ml_pipeline/setup.py --create-sample-dataset
```

### 3. Verify Setup

```bash
python ml_pipeline/setup.py
```

### 4. Train Model

```bash
python ml_pipeline/train.py
```

**Training takes:**
- CPU: 2-6 hours
- GPU: 30 minutes - 2 hours

### 5. Make Predictions

```bash
# Single image
python ml_pipeline/predict.py test_image.jpg

# With visualization
python ml_pipeline/predict.py test_image.jpg --gradcam --output viz.png
```

### 6. Launch Web App

```bash
streamlit run ml_pipeline/streamlit_app.py
```

## Troubleshooting Installation

### Issue: "pip not recognized"

**Solution:**
```bash
# Use python -m pip
python -m pip install -r ml_pipeline/requirements.txt

# Or pip3
pip3 install -r ml_pipeline/requirements.txt
```

### Issue: "Permission denied"

**Solution (Windows):**
```bash
# Run as Administrator, or use --user flag
pip install --user -r ml_pipeline/requirements.txt
```

**Solution (Linux/Mac):**
```bash
# Use sudo or --user
sudo pip install -r ml_pipeline/requirements.txt
# Or
pip install --user -r ml_pipeline/requirements.txt
```

### Issue: "TensorFlow installation fails"

**Solution:**
```bash
# Install TensorFlow separately first
pip install tensorflow==2.15.0

# Then install other requirements
pip install numpy Pillow matplotlib seaborn scikit-learn
```

### Issue: "Slow installation"

**Solution:**
```bash
# Use faster mirror (India)
pip install -r ml_pipeline/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Or use conda
conda install tensorflow numpy pillow matplotlib seaborn scikit-learn
```

### Issue: "Out of memory during installation"

**Solution:**
```bash
# Install packages one by one
pip install numpy
pip install Pillow
pip install scikit-learn
pip install matplotlib
pip install seaborn
pip install tensorflow
```

## Verification Checklist

After installation, verify:

- [ ] `python -c "import tensorflow; print(tensorflow.__version__)"` works
- [ ] `python -c "import ml_pipeline; print('OK')"` works
- [ ] `python ml_pipeline/test_pipeline.py` shows 6/6 tests passed
- [ ] `python ml_pipeline/setup.py` shows "Setup complete"
- [ ] Dataset directory exists with class folders
- [ ] Models directory exists

## System Requirements

### Minimum Requirements
- Python 3.10+
- 8GB RAM
- 10GB free disk space
- CPU (training will be slow)

### Recommended Requirements
- Python 3.10+
- 16GB RAM
- 20GB free disk space
- NVIDIA GPU with CUDA (for faster training)

## Next Steps After Installation

1. **Prepare your dataset** in `dataset/` folder
2. **Run setup check:** `python ml_pipeline/setup.py`
3. **Train the model:** `python ml_pipeline/train.py`
4. **Test prediction:** `python ml_pipeline/predict.py <image>`
5. **Launch web app:** `streamlit run ml_pipeline/streamlit_app.py`

## Getting Help

If you encounter issues:

1. Check the error message carefully
2. Review `GETTING_STARTED.md` troubleshooting section
3. Ensure all dependencies are installed: `pip list`
4. Check Python version: `python --version` (should be 3.10+)
5. Try installing in a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r ml_pipeline/requirements.txt
   ```

## Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r ml_pipeline/requirements.txt

# Deactivate when done
deactivate
```

## Quick Test

After installation, run this quick test:

```bash
python -c "
from ml_pipeline import create_model
import tensorflow as tf

# Create test model
model = create_model(num_classes=5)
print('✅ Model created successfully')
print(f'Parameters: {model.model.count_params():,}')

# Test prediction
dummy_input = tf.random.normal((1, 224, 224, 3))
pred = model.model.predict(dummy_input, verbose=0)
print(f'✅ Prediction works: {pred.shape}')
print('✅ Pipeline is ready!')
"
```

---

**Remember:** The test failures shown are expected before installing dependencies. Once you run `pip install -r ml_pipeline/requirements.txt`, all tests should pass!