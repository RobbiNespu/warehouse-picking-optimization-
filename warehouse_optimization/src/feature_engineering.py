#!/usr/bin/env python3
"""
Feature Engineering Script for Warehouse Picking Optimization
This script performs the same operations as the Week 2 notebook but as a standalone script.
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# Create data directory if it doesn't exist
os.makedirs('../data', exist_ok=True)

# Load datasets
print("Loading datasets...")
customer_orders = pd.read_csv('../../Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company/Customer_Order.csv', sep=';')
picking_waves = pd.read_csv('../../Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company/Picking_Wave.csv', sep=';')
products = pd.read_csv('../../Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company/Product.csv', sep=';')

# Convert creationDate to datetime
customer_orders['creationDate'] = pd.to_datetime(customer_orders['creationDate'], format='%d/%m/%Y %H:%M')

print("Datasets loaded successfully!")

# Standardize column names for customer orders
customer_orders_standard = customer_orders.rename(columns={
    'codCustomer': 'customer_id',
    'orderNumber': 'order_id',
    'orderToCollect': 'order_line',
    'Reference': 'sku_id',
    'Size (US)': 'size_us',
    'quantity (units)': 'quantity',
    'creationDate': 'timestamp',
    'waveNumber': 'wave_id',
    'operator': 'operator_id'
})

# Standardize column names for picking waves
picking_waves_standard = picking_waves.rename(columns={
    'waveNumber': 'wave_id',
    'reference': 'sku_id',
    'Size (US)': 'size_us',
    'quantityToPick (units)': 'quantity_to_pick',
    'locations': 'location',
    'operator': 'operator_id'
})

# Standardize column names for products
products_standard = products.rename(columns={
    'Reference': 'sku_id',
    'ABCCOD': 'abc_code',
    'Sector': 'sector'
})

print("Column names standardized successfully!")

# Merge customer orders with product information
customer_orders_enriched = customer_orders_standard.merge(
    products_standard, 
    on='sku_id', 
    how='left'
)

# Calculate order sequence for each customer
customer_orders_enriched = customer_orders_enriched.sort_values(['customer_id', 'timestamp'])
customer_orders_enriched['order_sequence'] = customer_orders_enriched.groupby('customer_id').cumcount() + 1

# Calculate time-based features
customer_orders_enriched = customer_orders_enriched.sort_values(['operator_id', 'timestamp'])
customer_orders_enriched['prev_timestamp'] = customer_orders_enriched.groupby('operator_id')['timestamp'].shift(1)
customer_orders_enriched['latency_sec'] = (customer_orders_enriched['timestamp'] - customer_orders_enriched['prev_timestamp']).dt.total_seconds()

# Calculate queue depth (number of orders in wave)
wave_order_counts = customer_orders_enriched.groupby('wave_id').size().reset_index()
wave_order_counts = wave_order_counts.rename(columns={0: 'wave_order_count'})
customer_orders_enriched = customer_orders_enriched.merge(wave_order_counts, on='wave_id', how='left')

# Calculate order size (number of lines per order)
order_line_counts = customer_orders_enriched.groupby('order_id').size().reset_index()
order_line_counts = order_line_counts.rename(columns={0: 'order_size'})
customer_orders_enriched = customer_orders_enriched.merge(order_line_counts, on='order_id', how='left')

# For residual calculation, we'll simulate based on expected vs actual quantity
# In a real scenario, this would come from tolerance rules or measurements
customer_orders_enriched['expected_quantity'] = customer_orders_enriched['quantity']  # Placeholder
customer_orders_enriched['actual_quantity'] = customer_orders_enriched['quantity']    # Placeholder
customer_orders_enriched['residual'] = customer_orders_enriched['actual_quantity'] - customer_orders_enriched['expected_quantity']

# For delta_weight, we'll simulate based on product characteristics
# In a real scenario, this would come from product weight data
customer_orders_enriched['unit_weight'] = np.random.uniform(0.1, 2.0, len(customer_orders_enriched))  # Simulated weight
customer_orders_enriched['delta_weight'] = customer_orders_enriched['quantity'] * customer_orders_enriched['unit_weight']

# For distance_walked, we'll simulate based on location changes
# In a real scenario, this would come from actual distance calculations between locations
customer_orders_enriched['distance_walked'] = np.random.uniform(10, 100, len(customer_orders_enriched))  # Simulated distance

print("Key features engineered successfully!")

# Event-level features (each row represents a picking event)
event_features = customer_orders_enriched[[
    'customer_id', 'order_id', 'order_line', 'sku_id', 'size_us', 'quantity',
    'timestamp', 'wave_id', 'operator_id', 'abc_code', 'sector',
    'latency_sec', 'residual', 'delta_weight', 'distance_walked'
]]

print("Event-level features created:")
print(event_features.head())
print(f"Shape: {event_features.shape}")

# Order-level features (aggregated from event-level data)
order_features = customer_orders_enriched.groupby('order_id').agg({
    'customer_id': 'first',
    'timestamp': 'first',  # Order creation time
    'wave_id': 'first',
    'operator_id': 'first',
    'quantity': 'sum',  # Total quantity in order
    'order_size': 'first',  # Number of lines in order
    'delta_weight': 'sum',  # Total weight of order
    'distance_walked': 'sum',  # Total distance for order
    'residual': 'mean',  # Average residual per order
    'latency_sec': 'mean'  # Average latency per order
}).reset_index()

# Add additional calculated features
order_features['order_hour'] = order_features['timestamp'].dt.hour
order_features['order_dow'] = order_features['timestamp'].dt.dayofweek

print("Order-level features created:")
print(order_features.head())
print(f"Shape: {order_features.shape}")

# Station/operator-level features (hourly aggregation)
customer_orders_enriched['hour'] = customer_orders_enriched['timestamp'].dt.hour
customer_orders_enriched['date'] = customer_orders_enriched['timestamp'].dt.date

station_hourly_features = customer_orders_enriched.groupby(['operator_id', 'date', 'hour']).agg({
    'order_id': 'nunique',  # Number of orders
    'sku_id': 'count',  # Number of picks
    'quantity': 'sum',  # Total quantity picked
    'delta_weight': 'sum',  # Total weight
    'distance_walked': 'sum',  # Total distance
    'latency_sec': 'mean',  # Average latency
    'residual': 'mean'  # Average residual
}).reset_index()

# Rename columns for clarity
station_hourly_features.rename(columns={
    'order_id': 'orders_count',
    'sku_id': 'picks_count',
    'quantity': 'total_quantity',
    'delta_weight': 'total_weight',
    'distance_walked': 'total_distance',
    'latency_sec': 'avg_latency',
    'residual': 'avg_residual'
}, inplace=True)

print("Station/operator-hourly features created:")
print(station_hourly_features.head())
print(f"Shape: {station_hourly_features.shape}")

# Save feature tables to CSV format
event_features.to_csv('../data/event_features.csv', index=False)
order_features.to_csv('../data/order_features.csv', index=False)
station_hourly_features.to_csv('../data/station_hourly_features.csv', index=False)

print("Feature tables saved successfully!")
print("- Event-level features: event_features.csv")
print("- Order-level features: order_features.csv")
print("- Station/hour-level features: station_hourly_features.csv")

print("\nFeature engineering completed!")