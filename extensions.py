import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        
        try:
             base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
             quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        if quote == base and quote:
            raise APIException(f'Введите различные валюты. Вы ввели одинаковые: {base}.')
        
        try:
             amount = float(amount) 
             
        
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        if amount < 0:
            raise APIException(f'Отрицательное количество валюты. Попробуйте еще раз')
        if amount == float('inf'):
            raise APIException(f'Вы ввели недопустимо длинное число')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]
        total_base = total_base * amount
        
        return total_base  
