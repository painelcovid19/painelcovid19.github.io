import csv
import json
import logging
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import sys
import os
from dotenv import load_dotenv, find_dotenv

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
    alagoinhas = [2900306,  290070, 290190, 290205,290220, 290700, 290750, 290960,  291050, 
        291060,  291370, 291590, 291650, 291790, 292330,292410, 292700, 292970,
    ]
    camacari = [290570, 290860, 291005, 292100, 292520, 293070, ]
    salvador = [290650, 291610, 291920, 291992, 292740,292860,292920, 292950, 292975, 293320, ]
    cruz_das_almas = [290485,290490, 290820, 290980, 291160, 292060, 292230, 292900,292960, ]
    santo_antonio_de_jesus =[290100,290230,290730, 290830, 291020, 291030, 291685, 291780, 291820,291880,
    292130, 292220, 292240, 292250, 292575, 292730,292850, 292870, 292910, 292940, 293210, 293317, ]

    list_of_microregion = [alagoinhas,salvador, cruz_das_almas, santo_antonio_de_jesus, camacari ]
    def macroregiao(code):
        macroregiao = ""
        for ibge_code in list_of_microregion[0]:
            if ibge_code == code:
                macroregiao = "Alagoinhas"
                return macroregiao
        for ibge_code in list_of_microregion[1]:
            if ibge_code == code:
                macroregiao = "Salvador"
                return macroregiao
        for ibge_code in list_of_microregion[2]:
            if ibge_code == code:
                macroregiao = "Cruz das almas"
                return macroregiao
        for ibge_code in list_of_microregion[3]:
            if ibge_code == code:
                macroregiao = "Santo Antônio de Jesus"
                return macroregiao
        for ibge_code in list_of_microregion[4]:
            if ibge_code == code:
                macroregiao = "Camaçari"
                return macroregiao
                

    with open(
        "data/df_dados_macro_regioes_baiha.csv", "w", newline="", encoding="utf-8"
    ) as csvDadosAcumulados:
        dadosAcumulados = csv.writer(csvDadosAcumulados)
        dadosAcumulados.writerow(
            [
                "city",
                "city_ibge_code",
                "macro_region",
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

        codigosIBG_BA = [2900306,  290070, 290190, 290205,290220, 290700, 290750, 290960,  291050, 
        291060,  291370, 291590, 291650, 291790, 292330,292410, 292700, 292970,290570, 290860, 
        291005, 292100, 292520, 293070,290650, 291610, 291920, 291992, 292740,292860,292920,
         292950, 292975, 293320,290485,290490, 290820, 290980, 291160, 292060, 292230, 292900,
         292960,290100,290230,290730, 290830, 291020, 291030, 291685, 291780, 291820,291880,
        292130, 292220, 292240, 292250, 292575, 292730,292850, 292870, 292910, 292940, 293210, 
        293317,
        ]

        # pegando os dados acumulados das cidades do Ceará
        filters_BA_acumulados = {"state": "BA", "is_last": True}
        data_BA_acumlados = api.data(dataset_slug, table_name, filters_BA_acumulados)
        for row in data_BA_acumlados:
            for cod in codigosIBG_BA:
                if row["city_ibge_code"] == cod:
                    city = row["city"]
                    # logging.info(f"Coletando dados de {city}")
                    city_ibge_code = row["city_ibge_code"]
                    macro_region = macroregiao(city_ibge_code)
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
                            macro_region,
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
