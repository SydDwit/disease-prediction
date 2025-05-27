# Disease Prediction Model Training

This README provides instructions for training the disease prediction model with your new dataset.

## Setup and Training Steps

1. **Setup the environment**:
   ```
   cd model_training
   pip install -r requirements_training.txt
   ```

2. **Copy the dataset files**:
   ```
   python setup_data.py
   ```
   This will copy the dataset files from the "new model" folder to the data directory.

3. **Train the model**:
   ```
   python train_model.py
   ```
   This will:
   - Train a new Random Forest model on your dataset
   - Save the model files to the backend/models directory in the format expected by the backend
   - Generate visualizations in the evaluation_report directory

4. **Update the database with new disease and symptom mappings**:
   ```
   cd ../utils
   python update_database.py
   ```
   This will:
   - Update the doctors in the database to match specialties needed for the new diseases
   - Update the symptoms in the database to match those in the new dataset
   - Map symptoms to appropriate medical specialties

5. **Start the backend**:
   ```
   cd ../backend
   python main.py
   ```

6. **Start the frontend** (in a new terminal):
   ```
   cd ../frontend
   npm run dev
   ```

## File Structure

- `model_training/train_model.py` - The main training script
- `data/` - Directory containing the dataset files
- `backend/models/` - Where the trained model is saved
- `evaluation_report/` - Contains visualizations and metrics from training
- `utils/update_database.py` - Script to update the database with new disease and symptom mappings

## Customization

If you want to use a different dataset, modify the `train_csv_path` parameter in the `train_and_save_model()` function call in `train_model.py`.

## Changes Made to Support the New Dataset

1. **Disease-to-Specialty Mapping**: Updated the mapping between diseases and medical specialties in `backend/disease_specialties.py`

2. **Doctor Specialties**: Updated the list of doctors to include specialists relevant to the diseases in the new dataset

3. **Symptom Mappings**: Added mappings between symptoms from the new dataset and appropriate medical specialties

These changes ensure that the system can correctly recommend doctors based on the symptoms and diseases in the new dataset. 