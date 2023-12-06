import requests
import os, random, string
from dotenv import load_dotenv

load_dotenv()


KEY = os.getenv('PAYSTACK_SECRET_KEY')


def initialize_transactions(email:str, amount:str, payment_id:str):
    headers = {
        'Authorization': f"Bearer {KEY}",
    }
        
    data = {
        'email':email,
        'amount':amount,
        'reference':payment_id,
    }

    url="https://api.paystack.co/transaction/initialize"

    response = requests.post(url=url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['data']['authorization_url']
    else:
        return response.json()['message']
    

def verify_payment(reference):
    headers = {
        'Authorization': f'Bearer {KEY}',
    }

    verify_payment_url = f'https://api.paystack.co/transaction/verify/{reference}'

    response = requests.get(verify_payment_url, headers=headers)

    if response.status_code == 200:
        payment_data = response.json()['data']
        return payment_data
    else:
        return None


def generate_payment_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
