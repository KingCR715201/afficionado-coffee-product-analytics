# Afficionado Coffee Sales Performance & Revenue Analytics Dashboard

## Project Overview

This project delivers a modern business intelligence solution for Afficionado Coffee. It enables decision-makers to monitor sales performance, identify top products, compare store revenue, and generate business recommendations through an interactive dashboard.

## Problem Statement

Afficionado Coffee collects transaction-level sales data across coffee products, categories, brands, and stores but lacks a centralized analytics platform to make data-driven inventory and promotional decisions.

## Objectives

- Analyze overall sales performance
- Identify top-selling and underperforming products
- Measure revenue contribution by product, category, and brand
- Compare sales performance across stores and time
- Support inventory optimization and promotional planning

## Features

- Executive KPI dashboard
- Product ranking and revenue contribution analysis
- Category and brand benchmarking
- Store performance and average order value analytics
- Customer type and payment method insights
- Pareto analysis for hero product identification
- Automated business recommendations
- Filtered dataset download

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Scikit-learn
- OpenPyXL

## Installation

1. Clone the repository or copy the project files.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

1. Place your sales data CSV file in the project folder as `sales_data.csv`.
2. Run the dashboard:

```bash
streamlit run streamlit_dashboard.py
```

3. Open the provided local URL in a browser.

## Folder Structure

- `coffee_sales_analysis.py` - data preprocessing, analytics, and insight generation
- `streamlit_dashboard.py` - complete interactive dashboard application
- `requirements.txt` - required Python packages
- `README.md` - project documentation
- `Deployment_Guide.md` - deployment instructions

## Dashboard Images Placeholder

Add dashboard screenshots here once the application is running:

- `screenshot_executive_dashboard.png`
- `screenshot_product_analytics.png`
- `screenshot_pareto_analysis.png`

## Future Scope

- Add predictive sales forecasting
- Integrate inventory and supply chain metrics
- Add user authentication and role-based access
- Expand sales funnel and campaign analytics
- Add spreadsheet upload and data refresh automation
