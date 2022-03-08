import http.client

conn = http.client.HTTPSConnection("api.pagerduty.com")

payload = "{\n  \"incident\": {\n    \"type\": \"incident_reference\",\n    \"status\": \"resolved\",\n    \"resolution\": \"resolved with the help of automated script (Author: Chetan Thakre)\"\n  }\n}"

headers = {
    'Content-Type': "application/json",
    'Accept': "application/vnd.pagerduty+json;version=2",
    'From': "email",
    'Authorization': "Token token="
    }
incident_id = ""
request = "/incidents/" + incident_id

conn.request("PUT", request, payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
