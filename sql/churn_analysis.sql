-- Premium Customer Churn Analysis
-- Assumed table: customer_churn

-- 1. Churn scorecard by segment and contract
SELECT
  segment,
  contract,
  COUNT(*) AS customers,
  AVG(churned) AS churn_rate,
  AVG(monthly_fee) AS avg_monthly_fee,
  AVG(nps_score) AS avg_nps,
  AVG(support_tickets) AS avg_support_tickets
FROM customer_churn
GROUP BY segment, contract
ORDER BY churn_rate DESC;

-- 2. Revenue at risk by segment
SELECT
  segment,
  SUM(CASE WHEN churned = 1 THEN monthly_fee ELSE 0 END) AS monthly_revenue_at_risk,
  AVG(CASE WHEN churned = 1 THEN nps_score END) AS churned_customer_avg_nps
FROM customer_churn
GROUP BY segment
ORDER BY monthly_revenue_at_risk DESC;

-- 3. High-friction customers
SELECT
  customer_id,
  segment,
  contract,
  monthly_fee,
  support_tickets,
  nps_score,
  last_login_days
FROM customer_churn
WHERE support_tickets >= 4 OR nps_score < 40 OR last_login_days >= 14
ORDER BY monthly_fee DESC;
