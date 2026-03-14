# Zomato Marketing Strategy - Marketing Analytics Case Study

This repository contains a complete analytics solution for the Brand Wars case on customer growth and retention at Zomato.

## Project Objective

Analyze customer behavior, campaign performance, discount usage, and repeat-order patterns to recommend how Zomato can optimize marketing spend and improve long-term customer value.

## What Is Included

- Full detailed report with business context, methodology, insights, and recommendations
- SQL KPI pack for dashboard-style analysis
- Python pipeline to generate KPI tables and repeat-order model outputs
- Generated output CSV and model metrics files

## Repository Structure

- Zomato_Marketing_Analytics_Report.md: Final detailed report
- marketing_kpis.py: Python pipeline for KPI generation and modeling
- marketing_kpis.sql: SQL KPI queries
- outputs/: Generated analysis tables and model outputs
- zomato dataset.xlsx: Source dataset

## Dataset Schema Used

The analysis uses these fields from the dataset:

- customer id, age, gender, city, zomato gold member
- order id, order value, discount amount, payment mode, delivery time mins, cuisine type
- campaign type, channel, coupon used, impressions, clicks, conversion flag
- repeat customer, orders last 30 days, avg order value, churn risk score

## Setup

Recommended environment:

- Python 3.10+
- pandas
- openpyxl
- scikit-learn

Install dependencies:

pip install pandas openpyxl scikit-learn

## How To Run

1. Keep the dataset file name as zomato dataset.xlsx in the project root.
2. Run:

python marketing_kpis.py

3. Check generated files inside outputs/.

## Generated Outputs

The Python pipeline creates:

- outputs/overall.csv
- outputs/high_value_segments.csv
- outputs/campaign_perf.csv
- outputs/discount_eff.csv
- outputs/retention_matrix.csv
- outputs/repeat_model_feature_importance.csv
- outputs/repeat_model_metrics.txt

## SQL Usage

Use marketing_kpis.sql after loading your data into a SQL table named zomato_raw with original column names.

The SQL pack includes:

- Overall business dashboard query
- High-value segment discovery query
- Campaign effectiveness query
- Discount efficiency query
- Repeat-driver diagnostic query
- Retention risk matrix query

## Key Business Takeaways

- Repeat rate is moderate, but discount spend is high and should be optimized.
- Campaign combinations that maximize conversion are not always the same as those that maximize repeat quality.
- City-level and segment-level targeting is necessary for better marketing ROI.
- Coupon strategy should be segment-led to reduce discount leakage.
- High Risk plus High Value users should be the top retention priority.
- Predictive signal for repeat behavior is weak in current data, so experiment-driven optimization is essential.

## Presentation Assets

This repository also includes submission materials:

- Zomato_BrandWars_2026.pptx
- Zomato_BrandWars_2026_submission.pptx
- ThePhoenix_BrandWars_Report.docx

## Author

Prepared for Brand Wars 2026 case submission.
