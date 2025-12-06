sales = [
    {"day": "Mon", "sales": 200},
    {"day": "Tue", "sales": 900},
    {"day": "Wed", "sales": 2000},
    {"day": "Thur", "sales":3500},
    {"day": "fri", "sales":500},
    {"day": "sat", "sales":1800},
    {"day": "sun", "sales":5000}
]
for row in sales:
    s = row["sales"]
    if s < 500:
        label = "Loss"
    elif s < 1500:
        label = "Low Margin"
    elif s < 3500:
        label = "Healthy"
    else:
        label = "Peak"
    print(row["day"], "=>", label)
  