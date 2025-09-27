# 📦 Warehouse Picking Optimization

A comprehensive data-driven analysis and optimization project for warehouse picking operations, achieving significant improvements in efficiency, workload balance, and operational fairness.

## 🎯 Key Results
- **25% reduction** in travel distances
- **30% improvement** in workload balance
- **20% increase** in throughput
- **35% improvement** in operational fairness

## 📊 Project Overview

This 6-week project analyzes warehouse picking operations using real-world data from a footwear manufacturing company, focusing on:

1. **Error Detection** – Identifying repark/pick mistakes using statistical models
2. **Batching & Assignment Optimization** – Grouping orders to minimize walking distances
3. **Fair Productivity Metrics** – Developing KPIs that account for downtime and walking
4. **Delay Prediction** – Detecting and forecasting operational delays

## 📁 Project Structure

```
warehouse_optimization/
├── notebooks/                     # Jupyter notebooks for weekly analysis
│   ├── week1_eda_profiling.ipynb         # Exploratory data analysis
│   ├── week2_feature_engineering.ipynb   # Feature creation and processing
│   ├── week3_baseline_rules_metrics.ipynb # Baseline metrics and rules
│   ├── week4_ml_models.ipynb             # Machine learning models
│   ├── week5_optimization_simulation.ipynb # Optimization algorithms
│   └── week6_visualization_report.ipynb   # Final visualizations
├── src/                           # Source code modules
├── data/                          # Data processing utilities
└── results/                       # Output files and models
```

## 📈 Dataset

- **32,634 orders** processed
- **122,370 picking events** analyzed
- **24 operators** tracked
- **208 unique SKUs**
- **Average order size**: 3.7 items

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Data-driven_to_warehouse_efficiency
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `warehouse_optimization/notebooks/` and run notebooks sequentially:
   - Start with `week1_eda_profiling.ipynb` for data exploration
   - Follow the weekly progression through `week6_visualization_report.ipynb`

## 📋 Analysis Workflow

### Week 1: Exploratory Data Analysis
- Data profiling and quality assessment
- Statistical summary and distributions
- Initial pattern identification

### Week 2: Feature Engineering
- Creation of productivity metrics
- Error detection features
- Temporal and spatial features

### Week 3: Baseline Rules & Metrics
- Business rule implementation
- Performance baseline establishment
- Error tolerance definitions

### Week 4: Machine Learning Models
- Predictive model development
- Error detection algorithms
- Performance optimization

### Week 5: Optimization & Simulation
- Batching optimization algorithms
- Route optimization
- Simulation of improved workflows

### Week 6: Visualization & Reporting
- Interactive dashboards
- Performance comparisons
- Final recommendations

## 🔍 Key Features

- **Error Detection System**: Statistical models to identify picking errors
- **Optimization Algorithms**: Advanced batching and routing optimization
- **Fair Metrics**: Productivity measures that account for operational constraints
- **Interactive Visualizations**: Comprehensive dashboards for operational insights

## 📊 Results & Impact

The analysis identified significant optimization opportunities:
- Reduced operator walking distances through intelligent batching
- Improved workload distribution across operators
- Enhanced error detection and prevention systems
- Data-driven insights for operational decision making

## 📄 Documentation

- [Final Analysis Report](FINAL_WAREHOUSE_OPTIMIZATION_REPORT.md) - Comprehensive project results
- [Project Overview](# 📦 Warehouse Picking Optimization.md) - Executive summary

## 🤝 Contributing

This project represents a completed analysis but can be extended for:
- Real-time optimization implementation
- Additional warehouse datasets
- Enhanced machine learning models
- Operational dashboard development

## 📧 Contact

For questions about this analysis or potential collaborations, please refer to the documentation or create an issue.