"""
Fast transfer learning training using MobileNetV2 + tf.data pipeline.
Set PLANTVILLAGE_DATASET_DIR to your dataset path.
"""

import os
import sys
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.environ.get(
    "PLANTVILLAGE_DATASET_DIR",
    os.path.join(BASE_DIR, "dataset", "PlantVillage"),
)
MODELS_DIR = os.path.join(BASE_DIR, "models")
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 6
AUTOTUNE = tf.data.AUTOTUNE


def get_class_names(data_dir: str) -> list[str]:
    entries = sorted(os.listdir(data_dir))
    classes = []
    for e in entries:
        p = os.path.join(data_dir, e)
        if os.path.isdir(p) and not e.startswith("."):
            classes.append(e)
    return classes


def normalize_label(name: str) -> str:
    name = name.replace("__", "___")
    if "___" not in name:
        name = name.replace("_", "___", 1)
    return name


def build_model(num_classes: int) -> models.Model:
    base = MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False

    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    model = models.Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    real_dir = DATASET_DIR
    if not os.path.isdir(real_dir):
        print(f"ERROR: Dataset not found: {real_dir}")
        sys.exit(1)

    base_name = os.path.basename(real_dir)
    nested = os.path.join(real_dir, base_name)
    if os.path.isdir(nested):
        subdirs_inside = [d for d in os.listdir(nested) if os.path.isdir(os.path.join(nested, d))]
        if len(subdirs_inside) >= 2:
            real_dir = nested
            print(f"Detected nested dataset folder, using: {real_dir}")

    class_names = get_class_names(real_dir)
    num_classes = len(class_names)
    print(f"Found {num_classes} classes:")
    for c in class_names:
        print(f"  {c}")

    print(f"\nLoading dataset with tf.data ({IMG_SIZE[0]}x{IMG_SIZE[1]})...")
    t0 = time.time()

    train_ds = tf.keras.utils.image_dataset_from_directory(
        real_dir,
        labels="inferred",
        label_mode="categorical",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=42,
        validation_split=0.1,
        subset="training",
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        real_dir,
        labels="inferred",
        label_mode="categorical",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=42,
        validation_split=0.1,
        subset="validation",
    )

    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ])

    def augment(image, label):
        image = data_augmentation(image)
        return image, label

    train_ds = train_ds.map(augment, num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)

    t1 = time.time()
    print(f"Dataset loaded in {t1-t0:.1f}s")

    print(f"\nBuilding model (MobileNetV2 transfer learning)...")
    model = build_model(num_classes)
    model.summary()

    print(f"\nTraining for {EPOCHS} epochs...")
    t0 = time.time()
    history = model.fit(
        train_ds,
        epochs=EPOCHS,
        validation_data=val_ds,
        verbose=1,
    )
    t1 = time.time()
    print(f"Training completed in {t1-t0:.1f}s")

    val_loss, val_acc = model.evaluate(val_ds, verbose=0)
    print(f"\nValidation accuracy: {val_acc:.4f}")
    print(f"Validation loss:     {val_loss:.4f}")

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    tflite_path = os.path.join(MODELS_DIR, "disease_model.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    print(f"\nTFLite model saved: {tflite_path} ({len(tflite_model) / 1024:.1f} KB)")

    labels_path = os.path.join(MODELS_DIR, "labels.txt")
    normalized = [normalize_label(c) for c in class_names]
    with open(labels_path, "w") as f:
        f.write("\n".join(normalized))
    print(f"Labels saved: {labels_path} ({len(normalized)} classes)")
    print("Done!")


if __name__ == "__main__":
    main()
