import requests
from datetime import datetime
import json
import pandas as pd


def get_api_data():
    #end point API
    API_URL = "https://api.waqi.info"
    #token de acesso
    token = "77d05ca5845b52922ee22f41d4386752adb7e9f5"
    #chave de cidade de medicao
    keyword = "Osasco, São Paulo, Brazil"
    #cidade medicao
    city = "osasco"

    #requisicao get para dados de medicao horaria
    jsson = feed(API_URL, token, city)

    # json_object = json.loads(jsson)

    print(json.dumps(jsson, indent=2))

    print(pd.json_normalize(jsson['pm10']))

def search(API_URL, token, keyword):   
    search_url = f"{API_URL}/v2/search/?token={token}&keyword={keyword}"
    response = requests.get(search_url)
    result = response.json()
    
    return (result)

def feed(API_URL, token, city):
    """
    retorna medicao horaria e previsao de AQI
    """
    search_url = f"{API_URL}/feed/{city}?token={token}"
    response = requests.get(search_url)
    result = response.json()
    
    return (result)

if __name__ == "__main__":
    get_api_data()