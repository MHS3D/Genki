import requests
import time
import json

url = "http://192.168.119.26:80"
unique_responses = {}

while True:
    try:
        response = requests.get(url)
        print(response.text)
        if response.status_code == 200:
            data = json.loads(response.text)
            
            # Merge the new data with the existing data
            for key, value in data.items():
                if key not in unique_responses:
                    unique_responses[key] = value
                else:
                    unique_responses[key].extend(value)
            
        else:
            print(f"Failed to get a valid response. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    time.sleep(0.2)  # Wait for 0.2 second before making the next request
    
    with open('data.json', 'w') as f:
        json.dump(unique_responses, f)