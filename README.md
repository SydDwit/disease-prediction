# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# Disease Prediction System

A full-stack application that uses machine learning to predict diseases based on symptoms, with a React frontend and Python backend.

## Project Structure

```
project-root/
│
├── frontend/                # Frontend React application
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   └── ...                  # Other frontend config files
│
├── backend/                 # Backend Python application
│   ├── models/              # Trained ML models
│   ├── main.py              # FastAPI application entry point
│   └── ...                  # Other backend files
│
├── data/                    # Dataset files
│   ├── Training.csv         # Training dataset
│   └── Testing.csv          # Testing dataset
│
├── model_training/          # Model training scripts
│   ├── train_model.py       # Main training script
│   ├── create_label_encoder.py
│   └── ...                  # Other training scripts
│
├── model_evaluation/        # Model evaluation scripts
│   ├── basic_model_evaluation.py
│   ├── run_all_evaluations.py
│   └── ...                  # Other evaluation scripts
│
├── visualization/           # Data visualization scripts
│   ├── bell_curve_graph.py
│   ├── generate_confusion_matrix.py
│   └── ...                  # Other visualization scripts
│
├── evaluation_report/       # Generated evaluation reports
│
├── utils/                   # Utility scripts
│   ├── setup_data.py
│   ├── update_database.py
│   └── ...                  # Other utility scripts
│
└── docs/                    # Documentation
    ├── TRAINING_README.md   # Training documentation
    └── ...                  # Other documentation files
```

## Directory Organization

The project has been reorganized for better maintainability:

1. **Frontend**: All React frontend code is now in the `frontend/` directory
2. **Backend**: All FastAPI backend code is in the `backend/` directory 
3. **Model Training**: Training scripts are in `model_training/`
4. **Model Evaluation**: Evaluation scripts are in `model_evaluation/`
5. **Visualization**: Visualization scripts are in `visualization/`
6. **Utilities**: Common utility scripts are in `utils/`
7. **Documentation**: All documentation is in `docs/`

This organization makes it easier to:
- Find relevant code for each part of the system
- Maintain separation of concerns
- Onboard new developers to the project
- Add new features in appropriate locations

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Setup

1. **Clone the repository**

2. **Setup the backend:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

3. **Setup the frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Training the model:**
   See [TRAINING_README.md](./docs/TRAINING_README.md) for detailed instructions.

## Features

- **Disease Prediction**: ML-based prediction from user symptoms
- **Doctor Recommendations**: Suggests specialists based on predicted diseases
- **Admin Dashboard**: Management of users, doctors, and system settings
- **Model Evaluation**: Comprehensive analysis of model performance

## Documentation

- [Training Documentation](./docs/TRAINING_README.md)
- [API Documentation](http://localhost:8000/docs) (when backend is running)

## Model Evaluation Report

The system now includes a comprehensive model evaluation report showing:

- **Confusion Matrix**: Visualizing the model's prediction accuracy across disease classes
- **Accuracy Metrics**: Details on precision, recall, and F1 scores
- **Feature Importance**: The most influential symptoms for disease prediction
- **Correlation Analysis**: Relationship between symptoms and diseases

## How to Access the Model Evaluation Report

There are two ways to access the model evaluation report:

1. **From the User Interface**:
   - After logging in, a "Model Analysis" link is available in the navigation bar
   - When making a disease prediction, a "View Detailed Model Analysis" button appears with the results

2. **Directly from Files**:
   - The report is available at: `public/evaluation_report/model_report.html`
   - Source files for the visualizations are in the `evaluation_report/` directory

## Running the Evaluation Scripts

If you want to regenerate the evaluation report:

```bash
# Run the basic model evaluation script
python basic_model_evaluation.py

# For more advanced analysis (may require fixing data issues)
python run_all_evaluations.py
```

## System Components

- **Frontend**: React application with user and admin interfaces
- **Backend**: FastAPI service for disease prediction and user management
- **Model**: Machine learning model for disease prediction
