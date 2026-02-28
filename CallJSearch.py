
import requests

url = "https://api.apilayer.com/jsearch/search"

params = {
    "query": "data engineer",
    "page": "1",
    "num_pages": "1",
    "date_posted": "all"
}

headers = {
    "apikey": "YOUR_API_KEY"
}

response = requests.get(url, headers=headers, params=params)

print(response.json())
