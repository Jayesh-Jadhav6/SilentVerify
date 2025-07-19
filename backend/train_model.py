import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # to save model

# Load data
df = pd.read_csv("user_data.csv")

# Convert JSON columns to feature counts
df["mouse_count"] = df["mouseMoves"].apply(lambda x: len(json.loads(x)))
df["click_count"] = df["clicks"].apply(lambda x: len(json.loads(x)))
df["scroll_count"] = df["scrolls"].apply(lambda x: len(json.loads(x)))

# Select features
X = df[["timeOnPage", "mouse_count", "click_count", "scroll_count"]]

# Convert label to numeric
df["label"] = df["label"].map({"human": 1, "bot": 0})  # bot data will come later
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, "passive_captcha_model.pkl")
print("✅ Model saved as passive_captcha_model.pkl")
