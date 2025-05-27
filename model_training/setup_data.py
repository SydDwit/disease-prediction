import os
import shutil

# Create directories if they don't exist
os.makedirs("data", exist_ok=True)

# Define paths with proper normalization
source_training = os.path.normpath("new model/data/Training.csv")
source_testing = os.path.normpath("new model/data/Testing.csv")
target_training = os.path.normpath("data/Training.csv")
target_testing = os.path.normpath("data/Testing.csv")

# Copy dataset files from the new model folder
print("Copying dataset files...")
shutil.copy(source_training, target_training)
shutil.copy(source_testing, target_testing)

print("Dataset files copied successfully!")
print("You can now run the training script with: python train_model.py") 