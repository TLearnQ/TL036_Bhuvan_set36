import json

data = [
    {"id": 1, "region": "south"},
    {"id": 2, "region": "east"},
    {"id": 3, "region": "south"},
    {"id": 4, "region": "east"},
    {"id": 5, "region": "south"},
    {"id": 6, "region": "south"}
]
south = []
east = []

for obj in data:
    if obj["region"] == "south":
        south.append(obj)
    else:
        east.append(obj)

with open("region_1.json", "w") as f:
    json.dump(south, f, indent=4)
with open("region_2.json", "w") as f:
    json.dump(east, f, indent=4)

print("region_1.json & region_2.json created")
