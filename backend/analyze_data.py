import pandas as pd
import json

df = pd.read_csv("user_data.csv")

print("✅ Total sessions logged:", len(df))
print("🕒 Avg time on page:", df["timeOnPage"].mean(), "seconds")

# Optional: check average number of mouse moves, clicks, scrolls
df["mouse_count"] = df["mouseMoves"].apply(lambda x: len(json.loads(x)))
df["click_count"] = df["clicks"].apply(lambda x: len(json.loads(x)))
df["scroll_count"] = df["scrolls"].apply(lambda x: len(json.loads(x)))

print("🖱️ Avg mouse moves:", df["mouse_count"].mean())
print("🖱️ Avg clicks:", df["click_count"].mean())
print("📜 Avg scrolls:", df["scroll_count"].mean())
