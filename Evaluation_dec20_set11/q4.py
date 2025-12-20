import requests
import json

TOKEN = "reqres-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
url = "https://reqres.in/api/users/2"
payload = {
    "job": "oracle"
}
response = requests.put(url, headers=headers, json=payload)
print("Status Code:", response.status_code)
print("Response JSON:")
print(json.dumps(response.json(), indent=4))
response_data = response.json()

if "udatedAt" in response_data:
    result = "pass: updatedAt field exists"
else:
    result = "fail: updatedAt field is missing"

print("\nAnalysis Result:")
print(result)
