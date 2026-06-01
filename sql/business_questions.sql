-- Customer Churn Analysis
-- Business KPI query examples. Adjust table and column names for a warehouse implementation.

-- 1. Preview source data
SELECT *
FROM sample_data
LIMIT 20;

-- 2. Count rows by a business dimension
SELECT
  dimension_column,
  COUNT(*) AS records
FROM sample_data
GROUP BY dimension_column
ORDER BY records DESC;

-- 3. Aggregate a primary numeric metric
SELECT
  dimension_column,
  SUM(metric_column) AS total_metric,
  AVG(metric_column) AS average_metric
FROM sample_data
GROUP BY dimension_column
ORDER BY total_metric DESC;

-- 4. Rank dimensions by business impact
SELECT
  dimension_column,
  SUM(metric_column) AS total_metric,
  RANK() OVER (ORDER BY SUM(metric_column) DESC) AS metric_rank
FROM sample_data
GROUP BY dimension_column;
