import requests

def get_ethereum_price(retry_count=3, retry_delay=1) -> float:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    for i in range(retry_count):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data["ethereum"]["usd"]

        if i < retry_count - 1:
            print(f"Failed to fetch data. Retrying in {retry_delay} seconds... (Attempt {i+1}/{retry_count})")
            time.sleep(retry_delay)
        else:
            raise Exception(f"Failed to fetch data after {retry_count} retries: {response.status_code}")
