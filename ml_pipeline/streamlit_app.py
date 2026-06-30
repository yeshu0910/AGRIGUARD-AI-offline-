"""
Streamlit application for AgriGuard AI crop disease detection.

This module provides a complete Streamlit web interface for the crop disease
detection system with image upload, prediction, and visualization features.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

import streamlit as st
from PIL import Image
import numpy as np

from ml_pipeline import create_predictor, format_prediction_for_streamlit
from ml_pipeline.config import get_config

# Configure page
st.set_page_config(
    page_title="AgriGuard AI - Crop Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f7f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
    }
    .recommendation {
        background-color: #f5f5f5;
        padding: 0.8rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model() -> Any:
    """
    Load and cache the prediction model.
    
    Returns:
        CropDiseasePredictor: Loaded predictor instance
    """
    try:
        predictor = create_predictor()
        return predictor
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.info("Please ensure the model is trained first by running: `python ml_pipeline/train.py`")
        return None


def display_header() -> None:
    """Display application header."""
    st.markdown('<p class="main-header">🌿 AgriGuard AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Offline Crop Disease Detection System</p>', unsafe_allow_html=True)
    st.markdown("---")


def display_sidebar(predictor: Any) -> Dict[str, Any]:
    """
    Display sidebar with settings and information.
    
    Args:
        predictor: Loaded predictor instance
    
    Returns:
        Dict: Settings dictionary
    """
    with st.sidebar:
        st.header("⚙️ Settings")
        
        settings = {}
        
        # Confidence threshold
        settings['confidence_threshold'] = st.slider(
            "Confidence Threshold",
            min_value=0.5,
            max_value=0.95,
            value=0.70,
            step=0.05,
            help="Minimum confidence for reliable prediction"
        )
        
        # Show Grad-CAM
        settings['show_gradcam'] = st.checkbox(
            "Show Grad-CAM Visualization",
            value=True,
            help="Display model attention heatmap"
        )
        
        # Show top predictions
        settings['show_top_k'] = st.slider(
            "Show Top K Predictions",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of top predictions to display"
        )
        
        st.markdown("---")
        
        # Model information
        if predictor:
            st.header("📊 Model Info")
            model_info = predictor.get_model_info()
            
            st.metric("Total Classes", model_info['num_classes'])
            st.metric("Model Parameters", f"{model_info['total_params']:,}")
            st.metric("Input Shape", f"{model_info['input_shape'][0]}x{model_info['input_shape'][1]}")
        
        st.markdown("---")
        
        # About section
        st.header("ℹ️ About")
        st.markdown("""
        **AgriGuard AI** uses deep learning to detect crop diseases from images.
        
        **Features:**
        - Offline inference
        - Multiple crop support
        - Confidence scoring
        - Treatment recommendations
        - Model explainability (Grad-CAM)
        
        **Technology:**
        - EfficientNetB0
        - TensorFlow/Keras
        - Transfer Learning
        """)
        
        return settings


def process_image(uploaded_file: Any) -> Optional[Image.Image]:
    """
    Process uploaded image file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        PIL.Image or None: Processed image
    """
    try:
        image = Image.open(uploaded_file)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None


def display_prediction_results(result: Dict[str, Any], settings: Dict[str, Any]) -> None:
    """
    Display prediction results in a formatted way.
    
    Args:
        result: Prediction result dictionary
        settings: Settings dictionary
    """
    # Main prediction
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🌾 Crop",
            value=result['crop']
        )
    
    with col2:
        st.metric(
            label="🦠 Disease",
            value=result['disease']
        )
    
    with col3:
        st.metric(
            label="🎯 Confidence",
            value=f"{result['confidence']:.2%}"
        )
    
    # Severity and prediction time
    col1, col2 = st.columns(2)
    
    with col1:
        severity_color = {
            'High': '🔴',
            'Medium': '🟡',
            'Low': '🟢',
            'Unknown': '⚪'
        }
        st.markdown(f"**Severity:** {severity_color.get(result['severity'], '⚪')} {result['severity']}")
    
    with col2:
        st.markdown(f"**Prediction Time:** ⏱️ {result['prediction_time']}")
    
    # Message for low confidence
    if result['message']:
        st.warning(f"⚠️ {result['message']}")
    else:
        st.success("✅ High confidence prediction")
    
    # Top K predictions
    if settings['show_top_k'] > 1:
        st.markdown("---")
        st.subheader(f"📊 Top {settings['show_top_k']} Predictions")
        
        for idx, pred in enumerate(result['top_5_predictions'][:settings['show_top_k']], 1):
            with st.expander(f"#{idx}: {pred['crop']} - {pred['disease']}"):
                # Progress bar for confidence
                st.progress(pred['confidence'])
                st.write(f"**Confidence:** {pred['confidence']:.2%}")
                st.write(f"**Severity:** {pred['severity']}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    for rec in result['recommendations']:
        st.markdown(f'<div class="recommendation">• {rec}</div>', unsafe_allow_html=True)


def display_gradcam(original_image: Image.Image, predictor: Any, result: Dict[str, Any]) -> None:
    """
    Display Grad-CAM visualization.
    
    Args:
        original_image: Original uploaded image
        predictor: Loaded predictor
        result: Prediction result
    """
    try:
        with st.spinner("Generating Grad-CAM visualization..."):
            # Get class index from top prediction
            class_idx = None
            if result['top_5_predictions']:
                top_class = result['top_5_predictions'][0]['class_name']
                class_idx = predictor.class_names.index(top_class)
            
            gradcam_img = predictor.generate_gradcam(
                original_image,
                class_idx=class_idx
            )
        
        st.markdown("---")
        st.subheader("🔍 Grad-CAM Visualization")
        st.markdown("*Heatmap showing regions the model focused on for prediction*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Image**")
            st.image(original_image, use_column_width=True)
        
        with col2:
            st.markdown("**Grad-CAM Overlay**")
            st.image(gradcam_img, use_column_width=True)
    
    except Exception as e:
        st.warning(f"Could not generate Grad-CAM: {str(e)}")


def main() -> None:
    """Main Streamlit application."""
    # Display header
    display_header()
    
    # Load model
    with st.spinner("Loading model..."):
        predictor = load_model()
    
    if not predictor:
        st.stop()
    
    # Display sidebar and get settings
    settings = display_sidebar(predictor)
    
    # Update confidence threshold if changed
    config = get_config()
    config.prediction.CONFIDENCE_THRESHOLD = settings['confidence_threshold']
    
    # Main content area
    st.markdown("## 📤 Upload Image")
    st.markdown("Upload an image of a crop (leaf, fruit, stem, flower, or root) for disease detection.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Supported formats: JPG, JPEG, PNG, BMP, TIFF"
    )
    
    # Example images section
    with st.expander("📸 Try Example Images"):
        st.markdown("If you don't have an image, you can download sample images from:")
        st.markdown("- [PlantVillage Dataset](https://data.mendeley.com/datasets/tywbtsjrjv/1)")
        st.markdown("- Or create your own dataset following the structure in the README")
    
    if uploaded_file is not None:
        # Process image
        image = process_image(uploaded_file)
        
        if image:
            # Display uploaded image
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Run prediction
            with st.spinner("Analyzing image..."):
                result = predictor.predict(image, return_top_k=settings['show_top_k'])
            
            # Display results
            st.markdown("---")
            st.markdown("## 📋 Prediction Results")
            display_prediction_results(result, settings)
            
            # Display Grad-CAM if enabled
            if settings['show_gradcam']:
                display_gradcam(image, predictor, result)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>AgriGuard AI - Offline Crop Disease Detection System</p>
        <p>Built with TensorFlow, EfficientNetB0, and Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()