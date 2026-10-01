import os
from typing import Any, Dict, List

import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "disease_classifier.joblib"
)

FEATURE_LIST_PATH = os.path.join(
    MODELS_DIR,
    "mlb.joblib"
)


# Educational condition -> specialist mapping
SPECIALIST_MAPPING = {
    "Common Cold": "General Physician",
    "Flu": "General Physician",
    "Malaria": "General Physician",
    "Acne": "Dermatologist",
    "Eczema": "Dermatologist",
    "Asthma": "Pulmonologist",
    "Bronchitis": "Pulmonologist",
    "Hypertension": "Cardiologist",
    "Coronary Artery Disease": "Cardiologist",
    "Migraine": "Neurologist",
}


DEFAULT_SPECIALIST = "General Physician"


class DiseasePredictor:

    def __init__(self):
        self.model = None
        self.feature_columns = None

        # Load the trained model
        self._load_artifacts()

    def _load_artifacts(self):
        """
        Load the trained ML model and feature list.
        """

        if not os.path.exists(MODEL_PATH) or not os.path.exists(
            FEATURE_LIST_PATH
        ):
            raise FileNotFoundError(
                "Model artifacts not found. Run 'python train_model.py' first."
            )

        self.model = joblib.load(MODEL_PATH)

        self.feature_columns = joblib.load(
            FEATURE_LIST_PATH
        )

    def predict(
        self,
        input_symptoms: List[str],
        top_n: int = 3
    ) -> Dict[str, Any]:
        """
        Accepts a list of symptom strings,
        converts them into binary features,
        and predicts possible conditions.
        """

        # ---------------------------------------------------------
        # STEP 1: Normalize the incoming symptoms
        # ---------------------------------------------------------

        normalized_inputs = {
            s.strip().lower().replace(" ", "_")
            for s in input_symptoms
        }

        # ---------------------------------------------------------
        # STEP 2: Convert symptoms into binary feature vector
        # ---------------------------------------------------------

        feature_vector = [
            1 if col in normalized_inputs else 0
            for col in self.feature_columns
        ]

        # ---------------------------------------------------------
        # STEP 3: Handle unknown / empty symptoms
        # ---------------------------------------------------------

        if sum(feature_vector) == 0:
            return {
                "predicted_condition": "Unknown",
                "confidence": 0.0,
                "recommended_specialist": DEFAULT_SPECIALIST,
                "top_matches": [],
                "disclaimer": (
                    "Educational screening tool only. "
                    "Not a medical diagnosis."
                ),
            }

        # ---------------------------------------------------------
        # STEP 4: Convert feature vector into DataFrame
        # ---------------------------------------------------------
        # The model was trained using named columns.
        # Using the same column names during prediction
        # removes the scikit-learn feature-name warning.

        feature_df = pd.DataFrame(
            [feature_vector],
            columns=self.feature_columns
        )

        # ---------------------------------------------------------
        # STEP 5: Get prediction probabilities
        # ---------------------------------------------------------

        probabilities = self.model.predict_proba(
            feature_df
        )[0]

        classes = self.model.classes_

        # ---------------------------------------------------------
        # STEP 6: Rank conditions by probability
        # ---------------------------------------------------------

        ranked_matches = sorted(
            zip(classes, probabilities),
            key=lambda x: x[1],
            reverse=True
        )

        # ---------------------------------------------------------
        # STEP 7: Get top prediction
        # ---------------------------------------------------------

        top_predicted_condition, top_prob = ranked_matches[0]

        # ---------------------------------------------------------
        # STEP 8: Find recommended specialist
        # ---------------------------------------------------------

        recommended_specialist = SPECIALIST_MAPPING.get(
            top_predicted_condition,
            DEFAULT_SPECIALIST
        )

        # ---------------------------------------------------------
        # STEP 9: Prepare top matches
        # ---------------------------------------------------------

        top_matches = [
            {
                "condition": str(cond),
                "probability": round(float(prob), 4)
            }
            for cond, prob in ranked_matches[:top_n]
            if prob > 0.0
        ]

        # ---------------------------------------------------------
        # STEP 10: Return final result
        # ---------------------------------------------------------

        return {
            "predicted_condition": str(top_predicted_condition),
            "confidence": round(float(top_prob), 4),
            "recommended_specialist": recommended_specialist,
            "top_matches": top_matches,
            "disclaimer": (
                "This is an educational screening system, "
                "not a real medical diagnosis."
            ),
        }


# =============================================================
# QUICK SANITY TEST
# =============================================================

if __name__ == "__main__":

    predictor = DiseasePredictor()

    sample_symptoms = [
        "headache",
        "nausea",
        "vomiting"
    ]

    result = predictor.predict(sample_symptoms)

    print("\n--- Predictor Sanity Test ---")

    print(
        "Input Symptoms:",
        sample_symptoms
    )

    print(
        "Predicted Condition:",
        result["predicted_condition"]
    )

    print(
        "Confidence:",
        f"{result['confidence'] * 100:.1f}%"
    )

    print(
        "Recommended Specialist:",
        result["recommended_specialist"]
    )

    print(
        "Top Matches:",
        result["top_matches"]
    )

    print(
        "Disclaimer:",
        result["disclaimer"]
    )

    print("-----------------------------\n")