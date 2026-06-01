# Customer Churn Analysis

Premium data analytics portfolio project focused on customer retention, churn risk, segmentation, and commercial action planning.

## Executive Scenario

A subscription business wants to reduce churn without wasting retention budget. The analytics team needs to identify high-risk segments, explain the main churn drivers, and produce a prioritized customer watchlist.

## Advanced Business Questions

- Which customer segments have the highest churn rate?
- Which behavioral and commercial factors are associated with churn?
- Which customers should be prioritized for retention outreach?
- What retention KPIs should leadership monitor monthly?
- Which actions are likely to reduce preventable churn?

## Premium Structure

- data/customer_churn.csv: enhanced synthetic customer dataset
- src/analysis.py: segmentation, model training, risk scoring, outputs
- src/dashboard.py: Streamlit dashboard for retention monitoring
- sql/churn_analysis.sql: analyst-ready churn queries
- docs/metric_dictionary.md: KPI and feature definitions
- reports/executive_summary.md: business recommendations

## How To Run

1. Install dependencies: pip install -r requirements.txt
2. Run the analysis pipeline: python src/analysis.py
3. Launch the dashboard: streamlit run src/dashboard.py

## Skills Demonstrated

Customer analytics, churn KPI design, feature engineering, classification modeling, customer segmentation, SQL, dashboarding, and stakeholder-ready storytelling.
