import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# Configs
DATASET_FOLDER = "data/train"
MODEL_NAME = "bin/sudoku_model.keras"
IMG_SIZE = (28, 28)
BATCH_SIZE = 32

def validate():
    # 1. Configure GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus: tf.config.experimental.set_memory_growth(gpu, True)
        except: pass

    # 2. Load model
    print(f"🧠 Loading {MODEL_NAME}...")
    model = tf.keras.models.load_model(MODEL_NAME)

    # 3. Load complete dataset
    print("📂 Reading images...")
    dataset = tf.keras.utils.image_dataset_from_directory(
        DATASET_FOLDER,
        shuffle=False, 
        image_size=IMG_SIZE,
        color_mode="grayscale",
        batch_size=BATCH_SIZE
    )

    class_names = dataset.class_names
    print(f"🏷️ Classes: {class_names}")

    # 4. Extract labels
    y_true = []
    y_pred = []

    print("⚡ Running inference...")
    
    # Iterate over all batches
    for images, labels in dataset:
        y_true.extend(labels.numpy())
        
        preds = model.predict(images, verbose=0)
        y_pred.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # 5. Generate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Check mistakes
    errors = np.sum(y_true != y_pred)
    total = len(y_true)
    accuracy = (total - errors) / total * 100

    print("\n" + "="*40)
    print(f"📊 Final Result: {accuracy:.2f}%")
    print(f"❌ Total Mistakes: {errors} of {total} images")
    print("="*40)

    # 6. Plot matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names)
    plt.xlabel('Prediction')
    plt.ylabel('Real')
    plt.title(f'Confusion Matrix (Acuracy: {accuracy:.2f}%)')
    plt.tight_layout()
    plt.savefig('training_pipeline/confusion_matrix.png')
    print("🖼️ Graph saved as confusion_matrix.png")

    # Detailed Report
    print("\nDetailed Report:")
    all_labels = range(len(class_names))
    print(classification_report(y_true, y_pred, target_names=class_names, labels=all_labels))

if __name__ == "__main__":
    validate()