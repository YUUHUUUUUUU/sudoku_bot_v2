import os
import matplotlib.pyplot as plt
import tensorflow as tf

# Configs
DATA_DIRECTORY = "data/train"
IMG_HEIGHT = 28
IMG_WIDTH = 28
BATCH_SIZE = 32
EPOCHS = 20 # Overkill

def main():
    # 1. GPU configuration
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"🚀 GPU Configured: {len(gpus)} units detected")
        except RuntimeError as e:
            print(f"⚠️ Error configuring the GPU: {e}")
    else:
        print("⚠️ GPU not detected. Training on the CPU (slower)")

    # 2. Loading data
    if not os.path.exists(DATA_DIRECTORY):
        print(f"❌ Error: '{DATA_DIRECTORY}' folder not found")
        return

    print("📂 Loading dataset...")
    
    # Training dataset (80%)
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIRECTORY,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode="grayscale",
        batch_size=BATCH_SIZE
    )

    # Validation (20%)
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIRECTORY,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode="grayscale",
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names
    print(f"🏷️ Classes detected: {class_names}")
    
    # Performance optimization
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # 3. Building the CNN
    print("🏗️ Building the architecture...")
    
    model = tf.keras.models.Sequential([
        # Entry layer + Normalization (0-255 -> 0-1)
        tf.keras.layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 1)),
        
        # Block 1
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        # Block 2
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        # Block 3
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        
        # Dense Classifier
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        
        # Output (probability)
        tf.keras.layers.Dense(len(class_names), activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])

    model.summary()

    # 4. Training
    print("🔥 Stating training...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS
    )

    # 5. Generating repport
    model_path = "bin/sudoku_model.keras"
    model.save(model_path)
    print(f"\n💾 Model saved as: {model_path}")

    # Salve the list of clases
    with open("bin/classes.txt", "w") as f:
        for name in class_names:
            f.write(f"{name}\n")
    print("📝 bin/classes.txt file created")

    # Generate performance graph
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(EPOCHS)

    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Accurracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Loss')
    
    plt.savefig('training_pipeline/training_results.png')
    print("📊 Graphs saved as 'resultado_treino.png'")

if __name__ == "__main__":
    main()