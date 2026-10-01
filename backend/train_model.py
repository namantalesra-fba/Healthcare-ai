import os
import joblib
import pandas as pd

from sklearn.naive_bayes import MultinomialNB


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
    "disease_classifier.joblib"
)

FEATURE_LIST_PATH = os.path.join(
    MODELS_DIR,
    "mlb.joblib"
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

    # Separate symptoms and disease
    feature_columns = [
        col for col in df.columns
        if col != "disease"
    ]

    X = df[feature_columns]
    y = df["disease"]

    # Shuffle the dataset
    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    # Manual 75% / 25% split
    split_index = int(len(df) * 0.75)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train = train_df[feature_columns]
    y_train = train_df["disease"]

    X_test = test_df[feature_columns]
    y_test = test_df["disease"]

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Create ML model
    print("\nTraining Multinomial Naive Bayes...")

    model = MultinomialNB()

    model.fit(
        X_train,
        y_train
    )

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate accuracy manually
    correct = sum(
        actual == predicted
        for actual, predicted in zip(
            y_test,
            predictions
        )
    )

    accuracy = correct / len(y_test)

    print("\n--- Training Results ---")
    print(
        f"Model Accuracy: {accuracy * 100:.2f}%"
    )
    print(
        f"Correct predictions: "
        f"{correct}/{len(y_test)}"
    )
    print("------------------------")

    # Save trained model
    joblib.dump(
        model,
        MODEL_PATH
    )

    # Save symptom feature names
    joblib.dump(
        feature_columns,
        FEATURE_LIST_PATH
    )

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nFeature list saved to:")
    print(FEATURE_LIST_PATH)

    print("\nTraining completed successfully!")


if __name__ == "__main__":
    train()