#!/usr/bin/env python3
"""
Optimization and Simulation Script for Warehouse Picking Optimization
This script implements the optimization algorithms from Week 5.
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

# Load the feature data
print("Loading feature data...")
event_features = pd.read_csv('../data/event_features_with_predictions.csv')
order_features = pd.read_csv('../data/order_features_with_predictions.csv')

print("Feature tables loaded successfully!")
print(f"Event features shape: {event_features.shape}")
print(f"Order features shape: {order_features.shape}")

# 1. Batching Optimizer Implementation (Clarke-Wright Savings Algorithm)
print("\n1. Implementing Batching Optimizer...")

# Prepare data for batching optimization
# Create order-SKU matrix for similarity calculation
order_skus = event_features[['order_id', 'sku_id']].drop_duplicates()

# For demonstration, let's work with a sample of orders
# Convert to list to avoid indexing issues
order_ids = order_skus['order_id'].tolist()
sample_orders = list(set(order_ids))[:100]  # Limit to 100 unique orders for performance

# Filter order_skus for sample orders
# Filter order_skus for sample orders
mask = [order_id in sample_orders for order_id in order_skus['order_id']]
order_skus_sample = order_skus[mask]

print(f"Working with {len(sample_orders)} orders for optimization")

# Create a simplified location-based distance matrix
# In a real scenario, this would come from actual warehouse layout data

# Simulate locations for each order (x, y coordinates)
np.random.seed(42)
order_locations = pd.DataFrame({
    'order_id': sample_orders,
    'x': np.random.uniform(0, 100, len(sample_orders)),
    'y': np.random.uniform(0, 100, len(sample_orders))
})

# Calculate pairwise distances between orders
def calculate_distance_matrix(locations_df):
    """Calculate Euclidean distance matrix between orders"""
    locations_array = locations_df[['x', 'y']].values
    n = len(locations_array)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            distance_matrix[i, j] = np.sqrt(
                (locations_array[i, 0] - locations_array[j, 0])**2 + 
                (locations_array[i, 1] - locations_array[j, 1])**2
            )
    
    return distance_matrix

distance_matrix = calculate_distance_matrix(order_locations)
print(f"Distance matrix shape: {distance_matrix.shape}")

# Clarke-Wright Savings Algorithm Implementation
def clarke_wright_savings(distance_matrix, depot_index=0, capacity_constraint=None):
    """
    Implement Clarke-Wright Savings Algorithm for Vehicle Routing
    """
    n = len(distance_matrix)
    
    # Calculate savings
    savings = []
    for i in range(1, n):  # Skip depot
        for j in range(i+1, n):
            saving = distance_matrix[depot_index, i] + distance_matrix[depot_index, j] - distance_matrix[i, j]
            savings.append((i, j, saving))
    
    # Sort savings in descending order
    savings.sort(key=lambda x: x[2], reverse=True)
    
    # Initialize routes - each customer in its own route
    routes = [[i] for i in range(1, n)]
    route_dict = {i: i-1 for i in range(1, n)}  # Map customer to route index
    
    # Merge routes based on savings
    for i, j, saving in savings:
        route_i = route_dict[i]
        route_j = route_dict[j]
        
        # Check if customers are in different routes
        if route_i != route_j:
            # Check capacity constraint if provided
            if capacity_constraint is not None:
                route_i_size = len(routes[route_i])
                route_j_size = len(routes[route_j])
                if route_i_size + route_j_size > capacity_constraint:
                    continue
            
            # Merge routes
            routes[route_i].extend(routes[route_j])
            for customer in routes[route_j]:
                route_dict[customer] = route_i
            routes[route_j] = []
    
    # Remove empty routes
    routes = [route for route in routes if route]
    
    return routes

# Apply Clarke-Wright algorithm
optimized_batches = clarke_wright_savings(distance_matrix, depot_index=0, capacity_constraint=10)

print(f"Number of optimized batches: {len(optimized_batches)}")
print(f"Average batch size: {np.mean([len(batch) for batch in optimized_batches]):.2f}")
print(f"Batch size distribution: {pd.Series([len(batch) for batch in optimized_batches]).describe()}")

# Compare with baseline random batching
def random_batching(orders, batch_size=10):
    """Random batching"""
    orders_list = list(orders)
    np.random.shuffle(orders_list)
    batches = [orders_list[i:i + batch_size] for i in range(0, len(orders_list), batch_size)]
    return batches

# Apply random batching
random_batches = random_batching(sample_orders, batch_size=10)

print(f"Number of random batches: {len(random_batches)}")
print(f"Average batch size (random): {np.mean([len(batch) for batch in random_batches]):.2f}")

# 2. Simulate Picker Assignments (Discrete-Event Simulation)
print("\n2. Simulating Picker Assignments...")

# For this example, we'll create a simple discrete-event simulation
# In a real scenario, we would use more sophisticated simulation libraries

# Simulate picker performance
np.random.seed(42)
operators = list(event_features['operator_id'].unique())
operator_performance = {}

for operator in operators:
    # Simulate performance metrics for each operator
    operator_performance[operator] = {
        'picks_per_hour': np.random.normal(50, 10),  # Mean picks per hour with std deviation
        'accuracy': np.random.normal(0.95, 0.02),    # Accuracy rate
        'avg_pick_time': np.random.normal(60, 10)    # Average time per pick in seconds
    }

# Simulate assignment of orders to operators
def simulate_picker_assignment(orders, operators, performance_data, batching_method='optimized'):
    """Simulate picker assignment"""
    if batching_method == 'optimized':
        batches = optimized_batches
    else:
        batches = random_batches
    
    # For simplicity, we'll just assign batches to operators in round-robin fashion
    assignments = []
    operator_idx = 0
    
    for batch in batches:
        operator = operators[operator_idx % len(operators)]
        assignments.append({
            'batch_id': len(assignments),
            'operator': operator,
            'orders': batch,
            'batch_size': len(batch),
            'estimated_time': len(batch) * performance_data[operator]['avg_pick_time']
        })
        operator_idx += 1
    
    return assignments

# Simulate with optimized batching
optimized_assignments = simulate_picker_assignment(
    sample_orders, operators, operator_performance, 'optimized'
)

# Simulate with random batching
random_assignments = simulate_picker_assignment(
    sample_orders, operators, operator_performance, 'random'
)

print(f"Optimized assignments: {len(optimized_assignments)} batches assigned to {len(operators)} operators")
print(f"Random assignments: {len(random_assignments)} batches assigned to {len(operators)} operators")

# 3. Measure Improvements in Throughput and Fairness
print("\n3. Measuring Improvements...")

# Calculate total estimated time for each method
total_time_optimized = sum([assignment['estimated_time'] for assignment in optimized_assignments])
total_time_random = sum([assignment['estimated_time'] for assignment in random_assignments])

# Calculate average batch size for each method
avg_batch_size_optimized = np.mean([assignment['batch_size'] for assignment in optimized_assignments])
avg_batch_size_random = np.mean([assignment['batch_size'] for assignment in random_assignments])

print("Performance Comparison:")
print(f"  Optimized - Total estimated time: {total_time_optimized:.2f} seconds")
print(f"  Random - Total estimated time: {total_time_random:.2f} seconds")
print(f"  Improvement: {((total_time_random - total_time_optimized) / total_time_random * 100):.2f}%")

print(f"  Optimized - Average batch size: {avg_batch_size_optimized:.2f}")
print(f"  Random - Average batch size: {avg_batch_size_random:.2f}")

# Calculate load balance (standard deviation of batch sizes)
batch_sizes_optimized = [assignment['batch_size'] for assignment in optimized_assignments]
batch_sizes_random = [assignment['batch_size'] for assignment in random_assignments]

std_optimized = np.std(batch_sizes_optimized)
std_random = np.std(batch_sizes_random)

print(f"  Optimized - Load balance (std dev): {std_optimized:.2f}")
print(f"  Random - Load balance (std dev): {std_random:.2f}")
print(f"  Load balance improvement: {((std_random - std_optimized) / std_random * 100):.2f}%")

# Save results
results_summary = {
    'batching_optimization': {
        'optimized_batches': len(optimized_batches),
        'random_batches': len(random_batches),
        'avg_batch_size_optimized': avg_batch_size_optimized,
        'avg_batch_size_random': avg_batch_size_random
    },
    'performance_comparison': {
        'total_time_optimized': total_time_optimized,
        'total_time_random': total_time_random,
        'time_improvement_percent': ((total_time_random - total_time_optimized) / total_time_random * 100),
        'load_balance_optimized': std_optimized,
        'load_balance_random': std_random,
        'load_balance_improvement_percent': ((std_random - std_optimized) / std_random * 100)
    }
}

# Save results to a text file
with open('../reports/optimization_results.txt', 'w') as f:
    f.write("Warehouse Picking Optimization - Results Summary\n")
    f.write("=" * 50 + "\n\n")
    
    f.write("1. Batching Optimization:\n")
    f.write(f"   Optimized batches: {results_summary['batching_optimization']['optimized_batches']}\n")
    f.write(f"   Random batches: {results_summary['batching_optimization']['random_batches']}\n")
    f.write(f"   Average batch size (optimized): {results_summary['batching_optimization']['avg_batch_size_optimized']:.2f}\n")
    f.write(f"   Average batch size (random): {results_summary['batching_optimization']['avg_batch_size_random']:.2f}\n\n")
    
    f.write("2. Performance Comparison:\n")
    f.write(f"   Total estimated time (optimized): {results_summary['performance_comparison']['total_time_optimized']:.2f} seconds\n")
    f.write(f"   Total estimated time (random): {results_summary['performance_comparison']['total_time_random']:.2f} seconds\n")
    f.write(f"   Time improvement: {results_summary['performance_comparison']['time_improvement_percent']:.2f}%\n")
    f.write(f"   Load balance (std dev) - optimized: {results_summary['performance_comparison']['load_balance_optimized']:.2f}\n")
    f.write(f"   Load balance (std dev) - random: {results_summary['performance_comparison']['load_balance_random']:.2f}\n")
    f.write(f"   Load balance improvement: {results_summary['performance_comparison']['load_balance_improvement_percent']:.2f}%\n")

print("\nOptimization and simulation completed!")
print("Results saved to:")
print("- ../reports/optimization_results.txt")