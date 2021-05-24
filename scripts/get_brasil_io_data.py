import csv
import json
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


class BrasilIO:

    base_url = "https://api.brasil.io/v1/"

    def __init__(self, auth_token):
        self.__auth_token = auth_token

    @property
    def headers(self):
        return {
            "User-Agent": "python-urllib/brasilio-client-0.1.0",
        }

    @property
    def api_headers(self):
        data = self.headers
        data.update({"Authorization": f"Token {self.__auth_token}"})
        return data

    def api_request(self, path, query_string=None):
        url = urljoin(self.base_url, path)
        if query_string:
            url += "?" + urlencode(query_string)
        request = Request(url, headers=self.api_headers)
        response = urlopen(request)
        return json.load(response)

    def data(self, dataset_slug, table_name, filters=None):
        url = f"dataset/{dataset_slug}/{table_name}/data/"
        filters = filters or {}
        filters["page"] = 1

        finished = False
        while not finished:
            response = self.api_request(url, filters)
            next_page = response.get("next", None)
            for row in response["results"]:
                yield row
            filters = {}
            url = next_page
            finished = next_page is None

    def download(self, dataset, table_name):
        url = f"https://data.brasil.io/dataset/{dataset}/{table_name}.csv.gz"
        request = Request(url, headers=self.headers)
        response = urlopen(request)
        return response


def main(api_key):
    logging.info('Iniciando script...')

    api = BrasilIO(api_key)
    dataset_slug = "covid19"
    table_name = "caso_full"

    directory = './data'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open('data/df_cidades_campi.csv', 'w', newline='',
              encoding='utf-8') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow([
            'city', 'city_ibge_code', 'date', 'last_available_confirmed',
            'last_available_confirmed_per_100k_inhabitants',
            'last_available_deaths', 'state', 'new_confirmed', 'new_deaths'
        ])

        # criando os filtros para cada cidade
        filters_Acarape = {"state": "CE", "is_last": False, "city": "Acarape"}
        filters_Redencao = {"state": "CE", "is_last": False, "city": "Redenção"}
        filters_STF = {"state": "BA", "is_last": False,"city": "São Francisco do Conde"}

        # criando uma array com todos os filtros
        filters = [filters_Acarape,filters_Redencao, filters_STF ]

        # array dos loggins 
        coletaDados = ['Coletando os dados de Acarape...', 
        'Coletando os dados de Redenção...', 
        'Coletando os dados de São Francisco do Conde...']

        # funcao busca dados, recebendo como parametro a array dos filtros
        def buscaDados(filters):

            for cont in range(0,3):
                logging.info(coletaDados[cont])
                data = api.data(dataset_slug, table_name, filters[cont])
                for row in data:
                    city = row['city']
                    city_ibge_code = row['city_ibge_code']
                    date = row['date']
                    last_available_confirmed = row['last_available_confirmed']
                    last_available_confirmed_per_100k_inhabitants = row[
                        'last_available_confirmed_per_100k_inhabitants']
                    last_available_deaths = row['last_available_deaths']
                    state = row['state']
                    new_confirmed = row['new_confirmed']
                    new_deaths = row['new_deaths']
                    csv_write.writerow([city, city_ibge_code, date, last_available_confirmed,
                                        last_available_confirmed_per_100k_inhabitants, last_available_deaths,
                                        state, new_confirmed, new_deaths])
        buscaDados(filters)

    logging.info('Dados coletados!')



if __name__ == "__main__":
    main(sys.argv[1])
