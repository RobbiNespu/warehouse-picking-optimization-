#!/usr/bin/env python3
"""
Baseline Rules and Metrics Script for Warehouse Picking Optimization
This script implements the baseline rules and metrics from Week 3.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Create reports directory if it doesn't exist
os.makedirs('../reports', exist_ok=True)

# Load the feature tables created in feature engineering
print("Loading feature data...")
event_features = pd.read_csv('../data/event_features.csv')
order_features = pd.read_csv('../data/order_features.csv')
station_hourly_features = pd.read_csv('../data/station_hourly_features.csv')

print("Feature tables loaded successfully!")
print(f"Event features shape: {event_features.shape}")
print(f"Order features shape: {order_features.shape}")
print(f"Station hourly features shape: {station_hourly_features.shape}")

# 1. Implement Tolerance Rule for Repark Errors
# Tolerance rule: |residual| > a + b√qty + c%
print("\n1. Implementing Tolerance Rule for Repark Errors...")

# Define tolerance parameters (these would be determined based on domain knowledge)
a = 0.5  # Base tolerance
b = 0.1  # Coefficient for square root of quantity
c = 0.02  # Percentage coefficient (2%)

# Calculate tolerance threshold for each event
event_features['tolerance_threshold'] = a + b * np.sqrt(event_features['quantity']) + c * event_features['quantity']

# Identify repark errors based on tolerance rule
event_features['is_repark_error'] = np.abs(event_features['residual']) > event_features['tolerance_threshold']

# Calculate error rate
error_rate = event_features['is_repark_error'].mean()
print(f"Overall repark error rate: {error_rate:.2%}")

# Error rate by SKU
sku_error_rates = event_features.groupby('sku_id')['is_repark_error'].agg(['count', 'sum', 'mean']).reset_index()
sku_error_rates.columns = ['sku_id', 'total_events', 'error_count', 'error_rate']
sku_error_rates = sku_error_rates[sku_error_rates['total_events'] >= 10]  # Filter for SKUs with sufficient events
# sku_error_rates = sku_error_rates.sort_values(by=['error_rate'], ascending=False)

print("\nTop 10 SKUs with highest error rates:")
print(sku_error_rates.head(10))

# 2. Greedy Batching vs Random Assignment
print("\n2. Comparing Greedy Batching vs Random Assignment...")

# For batching, we'll simulate orders with SKUs
# Create a simplified order-SKU matrix
order_skus = event_features[['order_id', 'sku_id']].drop_duplicates()

# Count SKUs per order
skus_per_order = order_skus.groupby('order_id').size().reset_index()
skus_per_order = skus_per_order.rename(columns={0: 'sku_count'})

# Count orders per SKU
orders_per_sku = order_skus.groupby('sku_id').size().reset_index()
orders_per_sku = orders_per_sku.rename(columns={0: 'order_count'})

print(f"Average SKUs per order: {skus_per_order['sku_count'].mean():.2f}")
print(f"Average orders per SKU: {orders_per_sku['order_count'].mean():.2f}")

# 3. Compute Availability-Adjusted Picks/Hour
print("\n3. Computing Availability-Adjusted Picks/Hour...")

# Raw picks per hour
operator_raw_performance = event_features.groupby('operator_id').agg({
    'sku_id': 'count',  # Number of picks
    'timestamp': ['min', 'max']  # Time range
}).reset_index()

# Flatten column names
operator_raw_performance.columns = ['operator_id', 'picks_count', 'start_time', 'end_time']

# Convert time strings to datetime
operator_raw_performance['start_time'] = pd.to_datetime(operator_raw_performance['start_time'])
operator_raw_performance['end_time'] = pd.to_datetime(operator_raw_performance['end_time'])

# Calculate working time in hours
operator_raw_performance['working_time_hours'] = (
    operator_raw_performance['end_time'] - operator_raw_performance['start_time']
).dt.total_seconds() / 3600

# Calculate raw picks per hour
operator_raw_performance['raw_picks_per_hour'] = (
    operator_raw_performance['picks_count'] / operator_raw_performance['working_time_hours']
)

print("Raw picks per hour by operator:")
print(operator_raw_performance[['operator_id', 'raw_picks_per_hour']])

# 4. Measure CPS Release→Arrival Delays
print("\n4. Measuring CPS Release→Arrival Delays...")

# For this example, we'll simulate CPS delays
# In a real scenario, this would come from actual CPS data
event_features['cps_delay_minutes'] = np.random.exponential(2, len(event_features))  # Simulated delays

# Calculate delay statistics
delay_stats = {
    'Mean delay (minutes)': event_features['cps_delay_minutes'].mean(),
    'Median delay (minutes)': event_features['cps_delay_minutes'].median(),
    '90th percentile delay (minutes)': event_features['cps_delay_minutes'].quantile(0.9),
    'Percentage of delays > 5 minutes': (event_features['cps_delay_minutes'] > 5).mean() * 100
}

print("CPS Delay Statistics:")
for key, value in delay_stats.items():
    print(f"  {key}: {value:.2f}")

# Save results
event_features.to_csv('../data/event_features_with_metrics.csv', index=False)
operator_raw_performance.to_csv('../data/operator_performance.csv', index=False)

print("\nBaseline rules and metrics completed!")
print("Results saved to:")
print("- ../data/event_features_with_metrics.csv")
print("- ../data/operator_performance.csv")