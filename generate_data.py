import pandas as pd
import numpy as np
import random
from pathlib import Path

# Make the data reproducible
np.random.seed(42)
random.seed(42)

# Generate 6,000 orders
n = 6000

categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports"]
regions = ["North", "South", "East", "West", "Central"]
cities = ["Hyderabad", "Bangalore", "Mumbai", "Delhi", "Chennai",
          "Pune", "Kolkata", "Jaipur", "Kochi", "Ahmedabad"]

products = {
    "Electronics": ["Laptop", "Headphones", "Smartphone", "Tablet"],
    "Fashion": ["Jeans", "Shoes", "T-Shirt", "Jacket"],
    "Home & Kitchen": ["Mixer", "Chair", "Cookware", "Lamp"],
    "Beauty": ["Face Cream", "Perfume", "Shampoo", "Makeup Kit"],
    "Sports": ["Football", "Yoga Mat", "Cricket Bat", "Dumbbells"]
}

rows = []

for i in range(n):
    category = random.choice(categories)
    product = random.choice(products[category])

    quantity = random.randint(1, 5)
    unit_price = random.randint(200, 15000)
    discount = random.choice([0, 5, 10, 15, 20])

    sales = quantity * unit_price * (1 - discount / 100)
    cost = sales * random.uniform(0.45, 0.80)
    profit = sales - cost

    rows.append({
        "Order_ID": f"ORD{i+1:05d}",
        "Order_Date": pd.Timestamp("2024-01-01") +
                      pd.Timedelta(days=random.randint(0, 730)),
        "Customer_ID": f"CUST{random.randint(1, 1500):04d}",
        "Region": random.choice(regions),
        "City": random.choice(cities),
        "Category": category,
        "Product": product,
        "Sales_Channel": random.choice(["Online", "Store", "Mobile App"]),
        "Customer_Segment": random.choice(["Regular", "Premium", "New"]),
        "Payment_Method": random.choice(["UPI", "Credit Card", "Debit Card", "Cash"]),
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": round(sales, 2),
        "Cost": round(cost, 2),
        "Profit": round(profit, 2),
        "Order_Status": random.choices(
            ["Delivered", "Cancelled", "Returned"],
            weights=[85, 8, 7]
        )[0]
    })

df = pd.DataFrame(rows)

# Save dataset inside the data folder
output_path = Path("data") / "ecommerce_orders.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print("Total records:", len(df))
print("Dataset saved at:", output_path)
print(df.head())