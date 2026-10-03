import os
import json
import math
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "symptoms_dataset.csv"
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "disease_classifier.json"
)


def train():

    print("Loading dataset...")

    os.makedirs(MODELS_DIR, exist_ok=True)

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    print(f"Dataset loaded: {len(df)} rows")

    feature_columns = [
        column
        for column in df.columns
        if column != "disease"
    ]

    # Shuffle dataset
    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    split_index = int(len(df) * 0.75)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    print(f"Training samples: {len(train_df)}")
    print(f"Testing samples: {len(test_df)}")

    diseases = sorted(
        train_df["disease"].unique()
    )

    total_training_samples = len(train_df)

    model = {
        "feature_columns": feature_columns,
        "classes": diseases,
        "class_counts": {},
        "feature_counts": {},
        "total_training_samples": total_training_samples
    }

    # =========================================================
    # COUNT EACH DISEASE
    # =========================================================

    for disease in diseases:

        count = len(
            train_df[
                train_df["disease"] == disease
            ]
        )

        model["class_counts"][disease] = count

    # =========================================================
    # COUNT SYMPTOMS FOR EACH DISEASE
    # =========================================================

    for disease in diseases:

        disease_rows = train_df[
            train_df["disease"] == disease
        ]

        model["feature_counts"][disease] = {}

        for feature in feature_columns:

            count = int(
                disease_rows[feature].sum()
            )

            model["feature_counts"][disease][feature] = count

    # =========================================================
    # TEST THE MODEL
    # =========================================================

    correct = 0

    print("\nTesting model...")

    for _, row in test_df.iterrows():

        symptoms = [
            feature
            for feature in feature_columns
            if row[feature] == 1
        ]

        prediction = predict_from_model(
            model,
            symptoms
        )

        actual = row["disease"]

        if prediction["condition"] == actual:
            correct += 1

        print(
            f"Actual: {actual:<25} "
            f"Predicted: {prediction['condition']}"
        )

    accuracy = (
        correct / len(test_df)
        if len(test_df) > 0
        else 0
    )

    print("\n-----------------------------")
    print("Training Results")
    print("-----------------------------")

    print(
        f"Model Accuracy: {accuracy * 100:.2f}%"
    )

    print(
        f"Correct predictions: "
        f"{correct}/{len(test_df)}"
    )

    # =========================================================
    # SAVE MODEL
    # =========================================================

    with open(
        MODEL_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            model,
            file,
            indent=4
        )

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nTraining completed successfully!")


def predict_from_model(
    model,
    symptoms
):

    feature_columns = model["feature_columns"]

    classes = model["classes"]

    class_counts = model["class_counts"]

    feature_counts = model["feature_counts"]

    total_samples = model["total_training_samples"]

    normalized_symptoms = {
        symptom.strip().lower().replace(" ", "_")
        for symptom in symptoms
    }

    scores = {}

    # =========================================================
    # CALCULATE NAIVE BAYES SCORE
    # =========================================================

    for disease in classes:

        disease_count = class_counts[disease]

        # Prior probability
        prior = (
            disease_count /
            total_samples
        )

        # Start with log probability
        log_probability = math.log(prior)

        # Number of training rows belonging
        # to this disease
        denominator = disease_count + 2

        for feature in feature_columns:

            feature_count = feature_counts[
                disease
            ][feature]

            # Laplace smoothing
            if feature in normalized_symptoms:

                probability = (
                    feature_count + 1
                ) / denominator

            else:

                probability = (
                    (disease_count - feature_count)
                    + 1
                ) / denominator

            log_probability += math.log(
                probability
            )

        scores[disease] = log_probability

    # =========================================================
    # NORMALIZE SCORES
    # =========================================================

    max_score = max(scores.values())

    exp_scores = {
        disease:
        math.exp(score - max_score)

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

    ranked = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True
    )

    condition = ranked[0][0]

    confidence = ranked[0][1]

    return {
        "condition": condition,
        "confidence": confidence,
        "probabilities": ranked
    }


if __name__ == "__main__":
    train()