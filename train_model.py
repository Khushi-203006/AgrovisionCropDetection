import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os, json

# --- Dataset Paths ---
dataset_path = r"D:\Khushi\project\mini project - 5th sem\agrovision_2\dataset"

train_dir = os.path.join(dataset_path, 'train')
val_dir   = os.path.join(dataset_path, 'val')
test_dir  = os.path.join(dataset_path, 'test')

# --- Image Parameters ---
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# --- Data Augmentation ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)
val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# --- Data Generators ---
train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)
val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)
test_gen = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# --- Save Class Indices for Flask App ---
class_indices = train_gen.class_indices
with open("class_indices.json", "w") as f:
    json.dump(class_indices, f)
print("📁 Saved class indices → class_indices.json")

# --- Model Architecture ---
num_classes = len(class_indices)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# --- Compile ---
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# --- Train ---
EPOCHS = 10  # you can increase to 20–30 if accuracy < 90%
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS
)

# --- Evaluate ---
test_loss, test_acc = model.evaluate(test_gen)
print(f"✅ Test Accuracy: {test_acc:.4f}")

# --- Save Model ---
model.save("plant_disease_model.h5")
print("💾 Model saved as plant_disease_model.h5")
