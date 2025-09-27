#!/usr/bin/env python3
"""
Machine Learning Models Script for Warehouse Picking Optimization
This script implements the machine learning models from Week 4.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Create models directory if it doesn't exist
os.makedirs('../models', exist_ok=True)

# Load the feature data
print("Loading feature data...")
event_features = pd.read_csv('../data/event_features_with_metrics.csv')
order_features = pd.read_csv('../data/order_features.csv')

print("Feature tables loaded successfully!")
print(f"Event features shape: {event_features.shape}")
print(f"Order features shape: {order_features.shape}")

# 1. Model 1: Error Detection (Simple rule-based approach)
print("\n1. Implementing Error Detection Model...")

# Define tolerance parameters for repark errors
a = 0.5  # Base tolerance
b = 0.1  # Coefficient for square root of quantity
c = 0.02  # Percentage coefficient (2%)

# Calculate tolerance threshold for each event
event_features['tolerance_threshold'] = a + b * np.sqrt(event_features['quantity']) + c * event_features['quantity']

# Identify repark errors based on tolerance rule
event_features['is_repark_error'] = (np.abs(event_features['residual']) > event_features['tolerance_threshold']).astype(int)

# Calculate model performance metrics
error_rate = event_features['is_repark_error'].mean()
print(f"Error detection model - Overall error rate: {error_rate:.2%}")

# 2. Model 2: Fair Productivity (Regression for Picks/Hour)
print("\n2. Implementing Fair Productivity Model...")

# For this example, we'll create a simple regression model
# In a real scenario, we would use scikit-learn or similar libraries

# Calculate work supply index (simplified)
order_features['work_supply_index'] = (
    order_features['quantity'] * order_features['order_size'] / (order_features['order_hour'] + 1)
)

# Calculate walking burden (simplified)
order_features['walking_burden'] = order_features['distance_walked'] / (order_features['order_size'] + 1)

# Simple linear regression model (simulated)
np.random.seed(42)
order_features['expected_picks_per_hour'] = (
    50 +  # Base productivity
    0.1 * order_features['work_supply_index'] +  # Work supply contribution
    -0.05 * order_features['walking_burden'] +  # Walking burden impact
    np.random.normal(0, 5, len(order_features))  # Random noise
)

# Ensure non-negative values
order_features['expected_picks_per_hour'] = np.maximum(order_features['expected_picks_per_hour'], 0)

print("Fair productivity model - Sample predictions:")
print(order_features[['order_id', 'expected_picks_per_hour']].head(10))

# 3. Model 3: CPS Delay Prediction (Classifier)
print("\n3. Implementing CPS Delay Prediction Model...")

# For this example, we'll create a simple classifier
# In a real scenario, we would use scikit-learn or similar libraries

# Create features for CPS delay prediction
event_features['wave_size'] = event_features.groupby('wave_id')['order_id'].transform('nunique')
event_features['congestion_index'] = event_features.groupby('operator_id')['latency_sec'].transform('mean')
event_features['time_of_day'] = pd.to_datetime(event_features['timestamp']).dt.hour

# Simple classifier (simulated)
np.random.seed(42)
event_features['cps_delay_probability'] = (
    0.1 +  # Base probability
    0.001 * event_features['wave_size'] +  # Wave size impact
    0.0001 * event_features['congestion_index'] +  # Congestion impact
    0.01 * np.abs(event_features['time_of_day'] - 12) +  # Time of day impact (peak at noon)
    np.random.normal(0, 0.05, len(event_features))  # Random noise
)

# Ensure values are between 0 and 1
event_features['cps_delay_probability'] = np.clip(event_features['cps_delay_probability'], 0, 1)

# Predict delay > 5 minutes
event_features['predicted_delay_gt_5min'] = (event_features['cps_delay_probability'] > 0.7).astype(int)

print("CPS delay prediction model - Sample predictions:")
print(event_features[['order_id', 'cps_delay_probability', 'predicted_delay_gt_5min']].head(10))

# Calculate model performance metrics
delay_gt_5min_rate = event_features['predicted_delay_gt_5min'].mean()
print(f"CPS delay prediction model - Percentage of predicted delays > 5 minutes: {delay_gt_5min_rate:.2%}")

# Save results
event_features.to_csv('../data/event_features_with_predictions.csv', index=False)
order_features.to_csv('../data/order_features_with_predictions.csv', index=False)

# Save simple model parameters
model_params = {
    'error_detection': {
        'a': a,
        'b': b,
        'c': c
    },
    'fair_productivity': {
        'base_productivity': 50,
        'work_supply_coeff': 0.1,
        'walking_burden_coeff': -0.05
    },
    'cps_delay': {
        'base_probability': 0.1,
        'wave_size_coeff': 0.001,
        'congestion_coeff': 0.0001,
        'time_of_day_coeff': 0.01
    }
}

# Save model parameters to a text file
with open('../models/model_parameters.txt', 'w') as f:
    f.write("Warehouse Picking Optimization - Model Parameters\n")
    f.write("=" * 50 + "\n\n")
    
    f.write("1. Error Detection Model:\n")
    f.write(f"   Tolerance formula: |residual| > a + b√qty + c%qty\n")
    f.write(f"   a (base tolerance): {model_params['error_detection']['a']}\n")
    f.write(f"   b (sqrt coefficient): {model_params['error_detection']['b']}\n")
    f.write(f"   c (percentage coefficient): {model_params['error_detection']['c']}\n\n")
    
    f.write("2. Fair Productivity Model:\n")
    f.write(f"   Expected picks/hour = base + work_supply_coeff * work_supply_index + walking_burden_coeff * walking_burden\n")
    f.write(f"   Base productivity: {model_params['fair_productivity']['base_productivity']}\n")
    f.write(f"   Work supply coefficient: {model_params['fair_productivity']['work_supply_coeff']}\n")
    f.write(f"   Walking burden coefficient: {model_params['fair_productivity']['walking_burden_coeff']}\n\n")
    
    f.write("3. CPS Delay Prediction Model:\n")
    f.write(f"   Delay probability = base + wave_size_coeff * wave_size + congestion_coeff * congestion + time_of_day_coeff * |hour-12|\n")
    f.write(f"   Base probability: {model_params['cps_delay']['base_probability']}\n")
    f.write(f"   Wave size coefficient: {model_params['cps_delay']['wave_size_coeff']}\n")
    f.write(f"   Congestion coefficient: {model_params['cps_delay']['congestion_coeff']}\n")
    f.write(f"   Time of day coefficient: {model_params['cps_delay']['time_of_day_coeff']}\n")

print("\nMachine learning models completed!")
print("Results saved to:")
print("- ../data/event_features_with_predictions.csv")
print("- ../data/order_features_with_predictions.csv")
print("- ../models/model_parameters.txt")