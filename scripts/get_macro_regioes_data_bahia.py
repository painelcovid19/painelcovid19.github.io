import csv
import json
import logging
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import sys
import os


# lendo o arquivo .env para obter a key
# load_dotenv(find_dotenv())
# api_key = os.getenv("my_API_key")

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
    logging.info("Inicioando o script")
    api = BrasilIO(api_key)
    dataset_slug = "covid19"
    table_name = "caso_full"

    directory = "./data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Para navegar pela API:
    # criando o dataset para as  cidades de redenção, Acarape e São Francisco do Conde
    # pegando os dados das cidades do Ceará
    # criando o dataset para as  cidades de redenção, Acarape e São Francisco do Conde

                

    with open(
        "data/df_dados_macro_regioes_bahia.csv", "w", newline="", encoding="utf-8"
    ) as csvDadosAcumulados:
        dadosAcumulados = csv.writer(csvDadosAcumulados)
        dadosAcumulados.writerow(
            [
                "city",
                "city_ibge_code",
                "date",
                "last_available_confirmed",
                "last_available_confirmed_per_100k_inhabitants",
                "last_available_deaths_per_100k_inhabitants",
                "estimated_population_2019",
                "last_available_deaths",
                "state",
                "new_confirmed",
                "new_deaths",
            ]
        )

        codigosIBG_BA = [
            2900702,
            2901106,
            2901700,
            2902054,
            2902203,
            2902302,
            2904852,
            2904902,
            2905701,
            2906501,
            2907509,
            2908200,	
            2908309,	
            2908507,	
            2908903,	
            2909802,	
            2910057,	
            2910800,	
            2911600,	
            2914505,	
            2916104,	
            2917805,	
            2919207,	
            2919926,	
            2920601,	
            2921005,	
            2922201,	
            2922300,	
            2922508,	
            2924108,	
            2925204,	
            2927309,	
            2927408,	
            2928604,	
            2928802,	
            2929008,
            2929107,	
            2929206,	
            2929305,	
            2929503,	
            2929602,	
            2929750,	
            2930709,	
            2931400,	
            2931707,	
            2933208,
        ]

        # pegando os dados acumulados das cidades do Ceará
        filters_BA_acumulados = {"state": "BA", "is_last": True}
        data_BA_acumlados = api.data(dataset_slug, table_name, filters_BA_acumulados)
        for row in data_BA_acumlados:
            for cod in codigosIBG_BA:
                if row["city_ibge_code"] == cod:
                    city = row["city"]
                    logging.info(f"Coletando dados de {city}")
                    city_ibge_code = row["city_ibge_code"]
                    date = row["date"]
                    last_available_confirmed = row["last_available_confirmed"]
                    last_available_confirmed_per_100k_inhabitants = row[
                        "last_available_confirmed_per_100k_inhabitants"
                    ]
                    estimated_population_2019 = row["estimated_population_2019"]
                    last_available_deaths = row["last_available_deaths"]
                    state = row["state"]
                    new_confirmed = row["new_confirmed"]
                    new_deaths = row["new_deaths"]
                    last_available_deaths_per_100k_inhabitants = round(
                        (last_available_deaths / estimated_population_2019 * 100000), 4
                    )
                    dadosAcumulados.writerow(
                        [
                            city,
                            city_ibge_code,
                            date,
                            last_available_confirmed,
                            last_available_confirmed_per_100k_inhabitants,
                            last_available_deaths_per_100k_inhabitants,
                            estimated_population_2019,
                            last_available_deaths,
                            state,
                            new_confirmed,
                            new_deaths,
                        ]
                    )
    logging.info("dados coletados")

if __name__ == "__main__":
    main(sys.argv[1])
