-- E-COMMERCE SALES & BUSINESS PERFORMANCE ANALYTICS

-- IMPORTANT:
-- Import ecommerce_orders.csv into SQLite.
-- Use the table name: orders


-- 1. Total Business Performance

SELECT
    ROUND(SUM(Sales), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    COUNT(DISTINCT Customer_ID) AS Unique_Customers
FROM orders;


-- 2. Monthly Revenue Analysis

SELECT
    strftime('%Y-%m', Order_Date) AS Month,
    ROUND(SUM(Sales), 2) AS Revenue
FROM orders
GROUP BY Month
ORDER BY Month;


-- 3. Category Performance

SELECT
    Category,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM orders
GROUP BY Category
ORDER BY Revenue DESC;


-- 4. Regional Performance

SELECT
    Region,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM orders
GROUP BY Region
ORDER BY Revenue DESC;


-- 5. Top 10 Products

SELECT
    Product,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Sales), 2) AS Revenue
FROM orders
GROUP BY Product
ORDER BY Revenue DESC
LIMIT 10;


-- 6. Customer Purchase Analysis

SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS Order_Count,
    ROUND(SUM(Sales), 2) AS Total_Spending
FROM orders
GROUP BY Customer_ID
ORDER BY Total_Spending DESC;


-- 7. Repeat Customer Analysis using CTE

WITH CustomerOrders AS (
    SELECT
        Customer_ID,
        COUNT(DISTINCT Order_ID) AS Order_Count
    FROM orders
    GROUP BY Customer_ID
)

SELECT
    CASE
        WHEN Order_Count > 1 THEN 'Repeat Customer'
        ELSE 'One-Time Customer'
    END AS Customer_Type,
    COUNT(*) AS Customer_Count
FROM CustomerOrders
GROUP BY Customer_Type;


-- 8. Sales Channel Analysis

SELECT
    Sales_Channel,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(
        SUM(Sales) * 100.0 /
        (SELECT SUM(Sales) FROM orders), 2
    ) AS Revenue_Percentage
FROM orders
GROUP BY Sales_Channel
ORDER BY Revenue DESC;


-- 9. Discount Analysis

SELECT
    Discount,
    COUNT(*) AS Order_Count,
    ROUND(AVG(Profit), 2) AS Average_Profit,
    ROUND(SUM(Sales), 2) AS Revenue
FROM orders
GROUP BY Discount
ORDER BY Discount;


-- 10. Order Status Analysis

SELECT
    Order_Status,
    COUNT(*) AS Order_Count
FROM orders
GROUP BY Order_Status;


-- 11. Category Ranking using Window Functions

WITH CategoryRevenue AS (
    SELECT
        Category,
        SUM(Sales) AS Revenue
    FROM orders
    GROUP BY Category
)

SELECT
    Category,
    ROUND(Revenue, 2) AS Revenue,
    DENSE_RANK() OVER (
        ORDER BY Revenue DESC
    ) AS Revenue_Rank
FROM CategoryRevenue;


-- 12. Month-over-Month Revenue Growth

WITH MonthlySales AS (
    SELECT
        strftime('%Y-%m', Order_Date) AS Month,
        SUM(Sales) AS Revenue
    FROM orders
    GROUP BY Month
),

SalesComparison AS (
    SELECT
        Month,
        Revenue,
        LAG(Revenue) OVER (
            ORDER BY Month
        ) AS Previous_Month_Revenue
    FROM MonthlySales
)

SELECT
    Month,
    ROUND(Revenue, 2) AS Revenue,
    ROUND(Previous_Month_Revenue, 2)
        AS Previous_Month_Revenue,
    ROUND(
        (Revenue - Previous_Month_Revenue)
        * 100.0 /
        NULLIF(Previous_Month_Revenue, 0),
        2
    ) AS Growth_Percentage
FROM SalesComparison
ORDER BY Month;


-- 13. Identify Loss-Making Products

SELECT
    Product,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM orders
GROUP BY Product
HAVING SUM(Profit) < 0
ORDER BY Profit ASC;