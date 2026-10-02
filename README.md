# LogisticsAnalytics_Week1

## Strategic Planning and Data Exploration in Logistics

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success)]

A practical **Logistics Data Analyst Internship – Week 1** project focused on strategic planning, KPI development, data-quality assessment, exploratory analysis, and a Python-based roadmap for predictive logistics analytics.

---

##  Project Overview

This project simulates a retail supply-chain analytics scenario in which an analytics team wants to understand shipment performance, identify operational patterns, and establish a foundation for future predictive analysis.

The project uses the publicly available **DataCo SMART Supply Chain for Big Data Analysis** dataset.

### Work completed

- Business scenario definition
- Problem statement
- Logistics KPI framework
- Public dataset research
- Data-quality assessment
- Data cleaning
- Feature engineering
- Exploratory data analysis
- Shipping-mode analysis
- Market-level analysis
- Data science methodology planning
- Predictive analytics roadmap
- Python implementation
- Strategic analytical roadmap
- Business impact assessment
- Final professional report

---

##  Business Problem

Retail supply chains can experience late shipments, schedule variance, cancellations, and differences in observed delivery performance across transportation modes and geographic markets.

The purpose of this project is to establish a structured analytical approach for understanding these patterns and preparing the foundation for future predictive logistics analysis.

The Week 1 analysis is primarily **descriptive and exploratory**. Observed relationships are not treated as proof of causation.

---

##  Project Objectives

1. Define a realistic logistics analytics scenario.
2. Identify relevant logistics KPIs.
3. Inspect and prepare a large supply-chain dataset.
4. Measure delivery performance.
5. Explore delivery patterns across shipping modes and markets.
6. Explain the use of data science methods in logistics.
7. Design an end-to-end Python analytics roadmap.
8. Produce a professional strategic planning report.

---

##  Dataset

### DataCo SMART Supply Chain for Big Data Analysis

The main transaction dataset contains information related to:

- Orders
- Customers
- Products
- Sales
- Shipping
- Delivery status
- Shipping modes
- Markets
- Regions
- Dates
- Geographic information

### Dataset Scale

| Metric | Value |
|---|---:|
| Records analyzed | 180,519 |
| Original columns | 53 |
| Duplicate rows | 0 |

### Source

**Mendeley Data – DataCo SMART Supply Chain for Big Data Analysis**

https://data.mendeley.com/datasets/8gx2fvg2k6/5

The original raw CSV is excluded from Git version control because of its size.

---

##  Data Preparation

The initial quality assessment identified highly incomplete fields.

| Field | Missing Values |
|---|---:|
| Product Description | 180,519 |
| Order Zipcode | 155,679 |
| Customer Lname | 8 |
| Customer Zipcode | 3 |

Highly incomplete fields that were not required for the core logistics analysis were removed.

Date fields were converted to appropriate date formats.

### Engineered Features

```text
Shipping Delay Days
= Actual Shipping Days - Scheduled Shipping Days

Is Delayed
= 1 when Delivery Status = Late delivery

Is On Time
= 1 when Delivery Status = Shipping on time

Is Advance
= 1 when Delivery Status = Advance shipping
