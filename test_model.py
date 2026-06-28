import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "AgriGuard", "backend"))
from detect import DiseaseDetector
from preprocess import preprocess

DATASET_ROOT = r"C:\Users\yeshw\OneDrive\Desktop\plant\PlantVillage\PlantVillage"

CLASS_DIRS = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___healthy",
    "Potato___Late_blight",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_healthy",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_mosaic_virus",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
]

def normalize_label(name: str) -> str:
    name = name.replace("__", "___")
    if "___" not in name:
        name = name.replace("_", "___", 1)
    return name

def get_test_images(dataset_root, class_dirs, samples_per_class=5):
    images = []
    for d in class_dirs:
        class_path = os.path.join(dataset_root, d)
        if not os.path.isdir(class_path):
            continue
        files = [f for f in os.listdir(class_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        for f in files[:samples_per_class]:
            images.append((os.path.join(class_path, f), normalize_label(d)))
    return images

def main():
    detector = DiseaseDetector()

    print("=" * 60)
    print("Model Input Shape:", detector.input_details[0]["shape"])
    print("Model Output Shape:", detector.output_details[0]["shape"])
    print("Number of labels:", len(detector.labels))
    print("=" * 60)

    test_images = get_test_images(DATASET_ROOT, CLASS_DIRS, samples_per_class=5)
    print(f"\nTesting on {len(test_images)} images ({len(CLASS_DIRS)} classes x 5 samples each)...\n")

    correct = 0
    total = 0
    errors = []

    for img_path, true_label in test_images:
        total += 1
        try:
            result = detector.predict(img_path)
            pred_label = result["class_index"]
            true_idx = detector.labels.index(true_label)
            is_correct = (pred_label == true_idx)
            if is_correct:
                correct += 1
            else:
                errors.append((os.path.basename(img_path), true_label, detector.labels[pred_label], result["confidence"]))
        except Exception as e:
            print(f"ERROR on {img_path}: {e}")

    accuracy = correct / total if total > 0 else 0
    print(f"\nAccuracy: {correct}/{total} = {accuracy:.2%}")

    if errors:
        print(f"\nMisclassified samples (showing first 10):")
        for fname, true_l, pred_l, conf in errors[:10]:
            print(f"  {fname}: true={true_l}, pred={pred_l}, conf={conf:.4f}")

    # Detailed top-5 for first image
    print("\n" + "=" * 60)
    print("Detailed top-5 predictions for first test image:")
    print("=" * 60)
    if test_images:
        img_path, true_label = test_images[0]
        print(f"Image: {os.path.basename(img_path)}")
        print(f"True label: {true_label}")
        print()
        
        input_data = preprocess(img_path, target_size=detector.input_size)
        detector.interpreter.set_tensor(detector.input_details[0]["index"], input_data)
        detector.interpreter.invoke()
        output = detector.interpreter.get_tensor(detector.output_details[0]["index"])
        scores = output[0]
        top5_idx = np.argsort(scores)[-5:][::-1]
        for i, idx in enumerate(top5_idx):
            print(f"  {i+1}. {detector.labels[idx]} (idx={idx}) - confidence: {scores[idx]:.4f}")

if __name__ == "__main__":
    main()
