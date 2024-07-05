import requests
from datetime import datetime
import json
import pandas as pd

import os

from pathlib import Path


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

    #pega dados de medicao iaqi horario
    df_iaqi = pd.json_normalize(jsson['data']['iaqi'])
    df_iaqi['AQUI'] = jsson['data']['aqi']

    #guarda data e hora
    data, hora = pd.json_normalize(jsson['data']['time'])['s'].values[0].split()

    #acrescenta data e hora no dataframe
    df_iaqi['data'] = data
    df_iaqi['hora'] = hora

    #tira .v
    df_iaqi.columns = df_iaqi.columns.str.rstrip('.v')

    #armazena dados de forecast
    df_forecast = pd.DataFrame()
    o3 = pd.json_normalize(jsson['data']['forecast']['daily']['o3'])
    pm10 = pd.json_normalize(jsson['data']['forecast']['daily']['pm10'])
    pm25 = pd.json_normalize(jsson['data']['forecast']['daily']['pm25'])

    o3['particulate'] = 'o3'
    pm10['particulate'] = 'pm10'
    pm25['particulate'] = 'pm25'

    #concatena tudo em um data frame
    df_forecast = pd.concat([o3, pm25, pm10], ignore_index=True)
    #coloca data e hora da previsao
    df_forecast['data_relatorio'] = data
    df_forecast['hora_relatorio'] = hora

    print("iniciando processo para armazenmaneto")

    #armazena forecast
    actual_folder = os.getcwd()
    
    path = Path(actual_folder)
    parent_folder = path.parent.absolute().as_posix()

    forecast_file = os.path.join(parent_folder, r"Dados/previsao/forecast.xlsx")
    df_forecast_hist = pd.read_excel(forecast_file)

    df_forecast_hist = pd.concat([df_forecast_hist, df_forecast], ignore_index=True)

    df_forecast_hist.to_excel(forecast_file, index=False)

    tempo_real_file = os.path.join(parent_folder, r"Dados/tempo_real/tempo_real.xlsx")
    tempo_real_file_hist = pd.read_excel(tempo_real_file)
    tempo_real_file_hist = pd.concat([tempo_real_file_hist, df_iaqi], ignore_index=True)
    tempo_real_file_hist.to_excel(tempo_real_file, index=False)

    print("Armazenamaneto feito com sucesso")

    

    return



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
    print("acessando API")
    response = requests.get(search_url)
    
    if response.status_code == 200:
        print("Request foi feita com sucesso")
    
    else:
        print("Problema na requisição, por favor verifique o acesso à API")
    
    result = response.json()
    
    return (result)

if __name__ == "__main__":
    get_api_data()