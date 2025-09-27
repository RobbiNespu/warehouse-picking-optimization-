
"""
Warehouse Picking Optimization Prototype
This script demonstrates a simple batching optimizer based on the Clarke-Wright savings algorithm.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

class WarehouseOptimizer:
    def __init__(self, capacity_constraint=10):
        self.capacity_constraint = capacity_constraint

    def calculate_savings(self, distance_matrix, depot_index=0):
        """Calculate savings for Clarke-Wright algorithm"""
        n = len(distance_matrix)
        savings = []

        for i in range(1, n):
            for j in range(i+1, n):
                saving = (distance_matrix[depot_index, i] + 
                         distance_matrix[depot_index, j] - 
                         distance_matrix[i, j])
                savings.append((i, j, saving))

        return sorted(savings, key=lambda x: x[2], reverse=True)

    def clarke_wright_algorithm(self, distance_matrix, depot_index=0):
        """Implement Clarke-Wright Savings Algorithm"""
        savings = self.calculate_savings(distance_matrix, depot_index)
        n = len(distance_matrix)

        # Initialize routes
        routes = [[i] for i in range(1, n)]
        route_dict = {i: i-1 for i in range(1, n)}

        # Merge routes based on savings
        for i, j, saving in savings:
            route_i = route_dict[i]
            route_j = route_dict[j]

            if route_i != route_j:
                # Check capacity constraint
                if (len(routes[route_i]) + len(routes[route_j]) <= 
                    self.capacity_constraint):
                    # Merge routes
                    routes[route_i].extend(routes[route_j])
                    for customer in routes[route_j]:
                        route_dict[customer] = route_i
                    routes[route_j] = []

        # Remove empty routes
        return [route for route in routes if route]

    def optimize_batching(self, orders_df, locations_df):
        """Optimize order batching based on locations"""
        # Merge order and location data
        merged_data = orders_df.merge(locations_df, on='order_id')

        # Create distance matrix
        locations_array = merged_data[['x', 'y']].values
        distance_matrix = euclidean_distances(locations_array)

        # Apply optimization
        optimized_batches = self.clarke_wright_algorithm(distance_matrix)

        # Map back to order IDs
        order_ids = merged_data['order_id'].tolist()
        batched_orders = []
        for batch in optimized_batches:
            batch_orders = [order_ids[i-1] for i in batch]  # Adjust for depot index
            batched_orders.append(batch_orders)

        return batched_orders

# Example usage
if __name__ == "__main__":
    # Sample data (in practice, this would come from your database)
    orders_data = pd.DataFrame({
        'order_id': [f'ORD{i:03d}' for i in range(1, 21)],
        'priority': np.random.choice(['High', 'Medium', 'Low'], 20)
    })

    locations_data = pd.DataFrame({
        'order_id': orders_data['order_id'],
        'x': np.random.uniform(0, 100, 20),
        'y': np.random.uniform(0, 100, 20)
    })

    # Initialize optimizer
    optimizer = WarehouseOptimizer(capacity_constraint=5)

    # Optimize batching
    optimized_batches = optimizer.optimize_batching(orders_data, locations_data)

    # Display results
    print("Optimized Batches:")
    for i, batch in enumerate(optimized_batches):
        print(f"  Batch {i+1}: {batch}")
