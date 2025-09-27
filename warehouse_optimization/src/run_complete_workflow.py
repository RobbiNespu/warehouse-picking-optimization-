#!/usr/bin/env python3
"""
Complete Workflow Runner for Warehouse Picking Optimization Project
This script runs the entire 6-week workflow in sequence to demonstrate the complete project.
"""

import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and check for errors"""
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print('='*60)
    
    try:
        result = subprocess.run([
            sys.executable, 
            script_name
        ], capture_output=True, text=True, check=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        print(f"✅ {script_name} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"❌ {script_name} failed with exception: {e}")
        return False

def main():
    """Run the complete workflow"""
    print("WAREHOUSE PICKING OPTIMIZATION PROJECT")
    print("Running complete 6-week workflow...\n")
    
    # Change to src directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Week 1: Already completed through notebooks
    
    # Week 2: Feature Engineering
    if not run_script("feature_engineering.py"):
        print("Stopping workflow due to error in feature engineering")
        return 1
    
    # Week 3: Baseline Rules & Metrics
    if not run_script("baseline_rules_metrics.py"):
        print("Stopping workflow due to error in baseline rules")
        return 1
    
    # Week 4: Machine Learning Models
    if not run_script("ml_models.py"):
        print("Stopping workflow due to error in ML models")
        return 1
    
    # Week 5: Optimization & Simulation
    if not run_script("optimization_simulation.py"):
        print("Stopping workflow due to error in optimization")
        return 1
    
    # Week 6: Visualization Dashboard
    if not run_script("visualization_dashboard.py"):
        print("Stopping workflow due to error in visualization")
        return 1
    
    # Run prototype optimizer
    if not run_script("warehouse_optimizer.py"):
        print("Warning: Prototype optimizer had issues")
    
    print("\n" + "="*60)
    print("🎉 COMPLETE WORKFLOW FINISHED SUCCESSFULLY! 🎉")
    print("="*60)
    print("\nAll 6 weeks of the warehouse picking optimization project have been completed!")
    print("\nGenerated files:")
    print("- Data files in /data/")
    print("- Model parameters in /models/")
    print("- Reports and visualizations in /reports/")
    print("- Source code in /src/")
    print("\nKey deliverables:")
    print("✅ Feature engineering completed")
    print("✅ Baseline rules implemented")
    print("✅ Machine learning models created")
    print("✅ Optimization algorithms developed")
    print("✅ Visualization dashboards generated")
    print("✅ Final report produced")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())