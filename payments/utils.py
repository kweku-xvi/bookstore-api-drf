import requests
import os
from dotenv import load_dotenv

load_dotenv()


KEY = os.getenv('PAYSTACK_SECRET_KEY')


def initialize_transactions(email:str, amount:str, order_id:str):
    headers = {
        'Authorization': f"Bearer {KEY}",
    }
        
    data = {
        'email':email,
        'amount':amount,
        'reference':order_id,
    }

    url="https://api.paystack.co/transaction/initialize"

    response = requests.post(url=url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['data']['authorization_url']
    else:
        return response.json()['message']
    