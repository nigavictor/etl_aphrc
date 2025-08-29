import json
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
import joblib

# __define-ocg__: OCG-compliant pipeline with filtering and logging

def load_data(path):
    with open(path) as f:
        logs = json.load(f)
    df = pd.json_normalize(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def transform(df):
    # Filter logs to only include the last 30 days
    cutoff = datetime.now() - timedelta(days=30)
    varFiltersCg = df[df["timestamp"] >= cutoff]  
    varOcg = varFiltersCg.copy()  
    varOcg["date"] = varOcg["timestamp"].dt.date

    # Aggregate daily active users
    daily = varOcg.groupby("date")["user_id"].nunique().reset_index()
    daily.columns = ["date", "daily_active_users"]
    daily["prev_day_users"] = daily["daily_active_users"].shift(1)
    return daily.dropna()

def train(data):
    X = data[["prev_day_users"]]
    y = data["daily_active_users"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, y_pred)
    print(f"✅ RMSE: {rmse:.2f}")
    return model

def save_model(model, path="model.pkl"):
    joblib.dump(model, path)
    print(f"✅ Model saved as {path}")

def load_model(path="model.pkl"):
    model = joblib.load(path)
    return model

def main():
    try:
        df = load_data("activity_logs.json")
        processed = transform(df)
        model = train(processed)
        save_model(model)
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")

if __name__ == "__main__":
    main()
