import joblib
import numpy as np
import os

class CivicMLPredictor:
    def __init__(self, model_path='model/model.pkl'):
        # Ensure path is relative to the script location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, model_path)
        self.model = joblib.load(full_path)
        
    def predict(self, text_embedding):
        """
        Predict whether the bill belongs to 'Housing and Economic Development'
        text_embedding: list or numpy array of length 384
        """
        X = np.array(text_embedding).reshape(1, -1)
        pred = self.model.predict(X)
        probability = self.model.predict_proba(X)[0][1] # Probability of class 1
        
        return {
            "prediction": bool(pred[0]),
            "probability": float(probability),
            "committee": "Housing and Economic Development" if pred[0] else "Other"
        }

if __name__ == '__main__':
    # Test inference
    predictor = CivicMLPredictor()
    # Dummy embedding for testing matching the 384-dimensional space
    dummy_embedding = np.random.rand(384).tolist()
    result = predictor.predict(dummy_embedding)
    print(f"Test Result: {result}")
