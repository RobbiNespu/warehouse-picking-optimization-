# 📦 Warehouse Picking Optimization

## Overview
This project explores **warehouse picking optimization** using open datasets (Instacart, Footwear,).  
The motivation comes from real-world warehouse systems like **WITRON DPS/OPM/CPS**, where issues include:

- Repark/pick errors not caught by weight checks.  
- CPS order release delays causing production downtime.  
- DPS productivity stats penalizing workers unfairly during low workload or long walking.  

We build **rules, models, and simulations** to propose improvements in error detection, batching, fairness, and flow management.

---

## Objectives
1. **Error Detection** – Identify repark/pick mistakes using weight + contextual features.  
2. **Batching & Assignment Optimization** – Group orders to minimize walking and balance load.  
3. **Fair Productivity Metrics** – Define KPIs that exclude downtime/walking.  
4. **Delay Prediction** – Detect and forecast CPS release→arrival delays.  

---

## Datasets
- **Instacart Market Basket (Kaggle)** – 3.4M orders, 50k products, 21 departments, 134 aisles.  
- **Footwear Warehouse Dataset** – order lines + picker routes, used for batching/walking analysis.  
 

These are proxies for warehouse logs and mapped to **order events, picks, totes, and delays**.

---

## Methodology
### 🔹 Data Processing
- Standardize schema: `order_id, sku_id, qty, ts`.  
- Feature engineering: residual weights, latency, walking distance, queue depth, SKU error rates.  

### 🔹 Baseline Rules
- Weight tolerance rule: `|residual| > a + b√qty + c%`.  
- Greedy order batching by SKU overlap.  
- Availability-adjusted picks/hour (exclude waiting/walking).  
- SLA check: release→arrival > threshold = delayed.  

### 🔹 Machine Learning Models
- **Error Detection**: XGBoost classifier on event features.  
- **Fair Productivity**: regression for expected picks/hour given workload.  
- **CPS Delay**: classifier predicting long release→arrival times.  
- **Batching Optimization**: clustering + graph-based assignment.  

### 🔹 Simulation
- Discrete-event simulation of order batching and picker assignment.  
- Compare walking distance and throughput vs baseline.

---

## Deliverables
- 📝 **Notebooks**: EDA, feature engineering, baseline rules, ML models, simulations.  
- 📊 **Dashboards**: error heatmap, batching efficiency, fair productivity, CPS delays.  
- 📑 **Report**: 2–3 page summary of findings and recommendations.  
- ⚙️ **Prototype optimizer**: script for smarter batching & assignment.  

---

## Timeline
- **Week 1:** Data setup & EDA  
- **Week 2:** Feature engineering  
- **Week 3:** Baseline rules  
- **Week 4:** ML models  
- **Week 5:** Optimization & simulation  
- **Week 6:** Dashboards + final report  

---

## Real-World Impact
- **DPS** – Reduce long walks, create fair productivity metrics.  
- **OPM/CPS** – Predict and prevent system delays and retries.  
- **Repark** – Catch misplacements early with smarter weight checks.  

This project serves as a **prototype** for applying data science to warehouse optimization, bridging **research datasets** and **industrial operations**.
