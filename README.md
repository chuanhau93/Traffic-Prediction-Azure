# Traffic Prediction - Azure Pipeline

An end-to-end data pipeline project: ingesting traffic data, exploring 
patterns, building a prediction model, and deploying it on Azure.

## Motivation
As a food delivery rider navigating Singapore's roads daily, I experience 
traffic congestion firsthand. This project explores whether vehicle traffic 
patterns can be understood and predicted using historical data - a step 
toward applying my AI/Cloud coursework to a real-world problem.

## Dataset
[Traffic Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/traffic-prediction-dataset) 
(Kaggle) - 48,120 hourly vehicle count readings across 4 road junctions, 
Nov 2015 to Jun 2017.

## Progress

### Phase 1: Exploratory Data Analysis (done)
- Extracted time-based features (hour, day of week, weekend flag) from raw timestamps
- Found that **Junction 1 shows a clear commuter pattern**: low traffic overnight, 
  rising sharply in the morning, peaking in the evening, and noticeably higher 
  on weekdays than weekends. Junctions 2-4 are flatter and less weekday-skewed, 
  suggesting different road types.
- See `eda_traffic.py` and `eda_chart.png`

### Phase 2: Modeling (done)
- Trained and compared two models to predict vehicle count from time-based features:
  - Linear Regression: MAE 9.04 vehicles
  - Random Forest: MAE 7.69 vehicles (selected model)
  - Baseline (predict average): MAE 15.13 vehicles
- Random Forest improved ~49% over baseline, and outperformed linear regression - 
  suggesting traffic patterns have non-linear structure (e.g. sharp rush-hour changes) 
  that a straight-line model can't capture.
- See `model_traffic.py` and `traffic_model.pkl`

### Phase 3: Deployment (planned)
- Deploy the trained model on Azure

## Files
- `traffic.csv` - raw dataset
- `eda_traffic.py` - data loading, feature engineering, and EDA
- `eda_chart.png` - hourly traffic pattern by junction
