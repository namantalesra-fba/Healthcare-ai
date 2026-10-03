import os
import json
import math

from typing import Any, Dict, List


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "disease_classifier.json"
)


# ============================================================
# SPECIALIST MAPPING
# ============================================================

SPECIALIST_MAPPING = {

    "Common Cold":
        "General Physician",

    "Flu":
        "General Physician",

    "Malaria":
        "General Physician",

    "Acne":
        "Dermatologist",

    "Eczema":
        "Dermatologist",

    "Asthma":
        "Pulmonologist",

    "Bronchitis":
        "Pulmonologist",

    "Hypertension":
        "Cardiologist",

    "Coronary Artery Disease":
        "Cardiologist",

    "Migraine":
        "Neurologist",
}


DEFAULT_SPECIALIST = "General Physician"


# ============================================================
# DISEASE PREDICTOR
# ============================================================

class DiseasePredictor:

    def __init__(self):

        self.model = None

        self.feature_columns = None

        self._load_model()


    # ========================================================
    # LOAD MODEL
    # ========================================================

    def _load_model(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(
                "Model not found. "
                "Run backend\\train_model.py first."
            )

        with open(
            MODEL_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            self.model = json.load(file)

        self.feature_columns = (
            self.model["feature_columns"]
        )


    # ========================================================
    # PREDICT
    # ========================================================

    def predict(
        self,
        input_symptoms: List[str],
        top_n: int = 3
    ) -> Dict[str, Any]:

        normalized_inputs = {

            symptom
            .strip()
            .lower()
            .replace(" ", "_")

            for symptom in input_symptoms
        }

        # ----------------------------------------------------
        # Empty input
        # ----------------------------------------------------

        if not normalized_inputs:

            return {

                "predicted_condition":
                    "Unknown",

                "confidence":
                    0.0,

                "recommended_specialist":
                    DEFAULT_SPECIALIST,

                "top_matches":
                    [],

                "disclaimer":
                    "Educational screening tool only. "
                    "Not a medical diagnosis."
            }


        # ----------------------------------------------------
        # Calculate probabilities
        # ----------------------------------------------------

        classes = self.model["classes"]

        class_counts = self.model[
            "class_counts"
        ]

        feature_counts = self.model[
            "feature_counts"
        ]

        total_samples = self.model[
            "total_training_samples"
        ]

        scores = {}


        for disease in classes:

            disease_count = class_counts[
                disease
            ]

            # Prior probability
            prior = (
                disease_count /
                total_samples
            )

            log_probability = math.log(
                prior
            )

            denominator = (
                disease_count + 2
            )


            for feature in self.feature_columns:

                feature_count = (
                    feature_counts[
                        disease
                    ][feature]
                )

                if feature in normalized_inputs:

                    probability = (
                        feature_count + 1
                    ) / denominator

                else:

                    probability = (
                        disease_count -
                        feature_count +
                        1
                    ) / denominator

                log_probability += math.log(
                    probability
                )


            scores[disease] = (
                log_probability
            )


        # ----------------------------------------------------
        # Convert scores to probabilities
        # ----------------------------------------------------

        max_score = max(
            scores.values()
        )

        exp_scores = {

            disease:
            math.exp(
                score - max_score
            )

            for disease, score
            in scores.items()
        }

        total_score = sum(
            exp_scores.values()
        )

        probabilities = {

            disease:
            value / total_score

            for disease, value
            in exp_scores.items()
        }


        # ----------------------------------------------------
        # Sort predictions
        # ----------------------------------------------------

        ranked_matches = sorted(

            probabilities.items(),

            key=lambda item:
                item[1],

            reverse=True
        )


        top_condition = (
            ranked_matches[0][0]
        )

        top_probability = (
            ranked_matches[0][1]
        )


        specialist = (
            SPECIALIST_MAPPING.get(
                top_condition,
                DEFAULT_SPECIALIST
            )
        )


        top_matches = [

            {
                "condition":
                    str(condition),

                "probability":
                    round(
                        float(probability),
                        4
                    )
            }

            for condition, probability
            in ranked_matches[:top_n]

            if probability > 0
        ]


        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------

        return {

            "predicted_condition":
                str(top_condition),

            "confidence":
                round(
                    float(top_probability),
                    4
                ),

            "recommended_specialist":
                specialist,

            "top_matches":
                top_matches,

            "disclaimer":
                "This is an educational "
                "screening system, not a "
                "real medical diagnosis."
        }


# ============================================================
# SANITY TEST
# ============================================================

if __name__ == "__main__":

    predictor = DiseasePredictor()

    sample_symptoms = [
        "headache",
        "nausea",
        "vomiting"
    ]

    result = predictor.predict(
        sample_symptoms
    )

    print(
        "\n--- Predictor Sanity Test ---"
    )

    print(
        "Input Symptoms:",
        sample_symptoms
    )

    print(
        "Predicted Condition:",
        result[
            "predicted_condition"
        ]
    )

    print(
        "Confidence:",
        f"{result['confidence'] * 100:.1f}%"
    )

    print(
        "Recommended Specialist:",
        result[
            "recommended_specialist"
        ]
    )

    print(
        "Top Matches:",
        result[
            "top_matches"
        ]
    )

    print(
        "Disclaimer:",
        result[
            "disclaimer"
        ]
    )

    print(
        "-----------------------------\n"
    )