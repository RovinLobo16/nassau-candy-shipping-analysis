# 🚚 Factory-to-Customer Shipping Route Efficiency Analysis

## Project Overview

This project analyzes shipping performance for **Nassau Candy Distributor**.

The dashboard provides insights into:

* Shipping lead time
* Route efficiency
* Geographic bottlenecks
* Shipping mode performance
* Factory-to-customer logistics patterns

The goal is to help identify **inefficient shipping routes and operational bottlenecks** using data-driven analysis.

---

# Dashboard Features

## 📊 Route Efficiency

* Average lead time per route
* Top 10 fastest routes
* Bottom 10 slowest routes
* Route efficiency score
* Route performance explorer

## 🌎 Geographic Analysis

* US shipping efficiency heatmap
* Bottleneck detection by state
* Geographic shipping performance comparison

## 🚛 Shipping Mode Comparison

* Standard vs Expedited shipping performance
* Lead time distribution analysis
* Shipping variability comparison

## 🏭 Factory Insights

* Factory locations visualization
* Product-to-factory mapping
* Factory distribution insights

## 📦 Order Timeline

* Shipment timeline visualization
* Lead-time variation over time
* Delivery trend analysis

## 🌐 Route Network Visualization

* Factory → Customer route network
* Logistics route mapping across the United States

## 🤖 AI Delay Prediction

The dashboard includes a **Machine Learning model** that predicts shipment delay risk based on:

* Region
* Shipping Mode
* Destination State
* Factory Source
* Units Ordered
* Sales Value

Model used:

Random Forest Classifier

---

# KPIs Implemented

The dashboard calculates key logistics metrics including:

* Shipping Lead Time
* Average Lead Time
* Route Volume
* Delay Frequency
* Route Efficiency Score
* Lead Time Variability
* Shipment Volume by Route

---

# Technologies Used

* Python
* Streamlit
* Pandas
* Plotly
* Scikit-learn

---

# Installation

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run 0_Dashboard.py

---

# Dataset

Nassau Candy Distributor shipping dataset containing information about:

* Orders
* Ship dates
* Shipping modes
* Regions
* States
* Sales
* Units

The dataset is used to analyze **factory-to-customer shipping route efficiency**.

---

# Project Structure

nassau-candy-shipping-analysis

0_Dashboard.py  
utils.py  
ml_model.py  
requirements.txt  

pages/

1_Correlation_Matrix.py  
2_Delay_Prediction_AI.py  
3_Geographic_Analysis.py  
4_Order_Timeline.py  
5_Product_Factory_Insights.py  
6_Route_Efficiency.py  
7_Route_Map.py  
8_Route_Network_Map.py  
9_Shipping_Mode_Performance.py  

---

# Business Impact

This analytics dashboard helps logistics teams:

* Identify inefficient shipping routes
* Detect delivery bottlenecks
* Improve shipping performance
* Optimize factory-to-customer distribution
* Make data-driven logistics decisions

---

# Author

Rovin Lobo
