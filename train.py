import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import joblib
import os

def main():
    print("Loading data...")
    # Load from the data directory
    X_df = pd.read_json('data/X.json')
    y_df = pd.read_json('data/y.json')

    print("Extracting features and labels...")
    X = np.array(X_df['text_embedding'].tolist())
    y = y_df['committee_bool'].values

    print("Building pipeline...")
    # Best model parameters from the grid search
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced', C=0.1, solver='lbfgs'))
    ])

    print("Training model on full dataset...")
    pipeline.fit(X, y)

    # Save model
    os.makedirs('model', exist_ok=True)
    model_path = 'model/model.pkl'
    print(f"Saving model to {model_path}...")
    joblib.dump(pipeline, model_path)
    print("Training complete!")

if __name__ == '__main__':
    main()
