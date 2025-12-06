
pages = [[1, 2], [3, 4], []]
combined = []
activity_log = []

for page in pages:
    activity_log.append("Reading new page")
    if not page:
        activity_log.append("No more data")
        break
    combined.extend(page)

print("Combined data")
print(combined)
print("Log:")
for item in activity_log:
    print(item)




                                   