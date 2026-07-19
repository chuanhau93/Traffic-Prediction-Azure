import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load the data with features already engineered in Phase 1
df = pd.read_csv('traffic.csv')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['hour'] = df['DateTime'].dt.hour
df['days_of_week'] = df['DateTime'].dt.dayofweek
df['is_weekend'] = df['days_of_week'].isin([5, 6]).astype(int)

# Junction is a category (1,2,3,4), not a ranked number -
# Junction 3 isn't "more" than Junction 1, they're just different roads.
# One-hot encoding turns this into separate yes/no columns per junction,
# so the model doesn't wrongly assume an order between them.
df = pd.get_dummies(df, columns = ['Junction'], prefix = 'Junction')

print(df.columns.tolist())
print(df.head())

# Define our inputs (X) and what we're trying to predict (y)
feature_cols = ['hour', 'days_of_week', 'is_weekend'] + [c for c in df.columns if c.startswith('Junction_')]
X = df[feature_cols]
y = df['Vehicles']

# Split data: 80% to train the model, 20% held back to test it honestly
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

# Train a simple linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set (data the model has never seen)
predictions = model.predict(X_test)

# Measure how far off, on average, the predictions were
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.2f} vehicles")

# Baseline: what if we just always predicted the average vehicle count?
baseline_prediction = y_train.mean()
baseline_mae = mean_absolute_error(y_test, [baseline_prediction] * len(y_test))
print(f"Baseline MAE (always predict the average): {baseline_mae:.2f} vehicles")
print(f"Our model's MAE: {mae:.2f} vehicles")

from sklearn.ensemble import RandomForestRegressor

# Random Forest: builds many decision trees and averages their predictions.
# Unlike linear regression, it can capture non-linear patterns -
# e.g. a sharp jump at 7am rather than assuming a smooth straight-line trend.
rf_model = RandomForestRegressor(n_estimators = 100, random_state=42)
rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_predictions)

print(f"Linear Regression MAE: {mae:.2f} vehicles")
print(f"Random Forest MAE:     {rf_mae:.2f} vehicles")
print(f"Baseline MAE:          {baseline_mae:.2f} vehicles")

import joblib

joblib.dump(rf_model, 'traffic_model.pkl')
print("Model saved to traffic_model.pkl")