import requests
import json

# Replace with your actual API key and endpoint
API_KEY = 'your_api_key_here'
BASE_URL = 'https://api.tradingwebsite.com/v1'

# Function to get market data
def get_market_data(symbol):
    endpoint = f"{BASE_URL}/marketdata/{symbol}"
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

# Function to place an order
def place_order(symbol, quantity, order_type, price=None):
    endpoint = f"{BASE_URL}/orders"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    order_data = {
        'symbol': symbol,
        'quantity': quantity,
        'type': order_type
    }
    if price:
        order_data['price'] = price

    response = requests.post(endpoint, headers=headers, data=json.dumps(order_data))
    return response.json()

# Example usage
symbol = 'AAPL'
market_data = get_market_data(symbol)
print("Market Data:", market_data)

order_response = place_order(symbol='AAPL', quantity=10, order_type='buy', price=150.00)
print("Order Response:", order_response)
