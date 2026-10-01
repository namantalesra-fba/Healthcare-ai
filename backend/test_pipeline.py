"""
Healthcare AI - Local Pipeline Verification Script

Connects nlp_processor.py and predictor.py to test the complete
symptom screening workflow without running the web server or database.
"""

from nlp_processor import extract_symptoms
from predictor import DiseasePredictor


def run_pipeline():
    print("=" * 60)
    print("          Healthcare AI - Local Screening Pipeline")
    print("=" * 60)

    # Load trained ML model
    try:
        predictor = DiseasePredictor()

    except FileNotFoundError as err:
        print(f"\n[Error] {err}")
        print("Please run train_model.py first.\n")
        return

    # Get user input
    user_input = input(
        "\nDescribe your symptoms (or press Enter for default test):\n> "
    ).strip()

    # Default test input
    if not user_input:
        user_input = (
            "I have a headache and I have been vomiting since morning."
        )

        print(
            f'Using default test sentence: "{user_input}"'
        )

    # --------------------------------------------------------
    # STEP 1 - NLP
    # --------------------------------------------------------

    print("\n" + "-" * 40)
    print("Step 1: NLP Symptom Extraction")
    print("-" * 40)

    detected_symptoms = extract_symptoms(user_input)

    print(f"User Input        : {user_input}")
    print(f"Extracted Symptoms: {detected_symptoms}")

    # No symptoms detected
    if not detected_symptoms:

        print(
            "\n[Notice] No recognized symptoms detected."
        )

        print(
            "Try terms such as cough, fever, headache, "
            "chest pain, vomiting, etc."
        )

        print("-" * 40)

        return

    # --------------------------------------------------------
    # STEP 2 - MACHINE LEARNING
    # --------------------------------------------------------

    print("\n" + "-" * 40)
    print("Step 2: Machine Learning Prediction")
    print("-" * 40)

    prediction_result = predictor.predict(
        detected_symptoms
    )

    # Get prediction values
    predicted_condition = (
        prediction_result.get(
            "predicted_condition"
        )
    )

    confidence_val = (
        prediction_result.get(
            "confidence",
            0.0
        )
    )

    specialist = (
        prediction_result.get(
            "recommended_specialist"
        )
    )

    top_matches = (
        prediction_result.get(
            "top_matches",
            []
        )
    )

    disclaimer = (
        prediction_result.get(
            "disclaimer"
        )
    )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(
        f"Predicted Condition   : {predicted_condition}"
    )

    print(
        f"Confidence Level      : "
        f"{confidence_val * 100:.2f}%"
    )

    print(
        f"Recommended Specialist: {specialist}"
    )

    print("\nTop Candidate Matches:")

    for rank, match in enumerate(
        top_matches,
        start=1
    ):

        condition = match["condition"]

        probability = (
            match["probability"] * 100
        )

        print(
            f"  {rank}. "
            f"{condition:<22} "
            f"({probability:.1f}%)"
        )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    print("\nDisclaimer:")

    print(
        f"  {disclaimer}"
    )

    print("=" * 60)
    print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_pipeline()