import csv
import json
import logging
import os
import sys
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

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
    logging.info("Iniciando script...")

    api = BrasilIO(api_key)
    dataset_slug = "covid19"
    table_name = "caso_full"

    directory = "./data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open("data/df_cidades_campi.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(
            [
                "city",
                "city_ibge_code",
                "date",
                "last_available_confirmed",
                "last_available_confirmed_per_100k_inhabitants",
                "last_available_deaths",
                "state",
                "new_confirmed",
                "new_deaths",
            ]
        )

        # criando os filtros para cada cidade
        filters_Acarape = {"state": "CE", "is_last": False, "city": "Acarape"}
        filters_Redencao = {"state": "CE", "is_last": False, "city": "Redenção"}
        filters_STF = {
            "state": "BA",
            "is_last": False,
            "city": "São Francisco do Conde",
        }

        # criando uma array com todos os filtros
        filters = [filters_Acarape, filters_Redencao, filters_STF]

        # funcao busca dados, recebendo como parametro a array dos filtros
        def buscaDados(filters):
            for filter in filters:
                logging.info(f"Coletando os dados de {filter['city']}...")
                data = api.data(dataset_slug, table_name, filter)
                for row in data:
                    city = row["city"]
                    city_ibge_code = row["city_ibge_code"]
                    date = row["date"]
                    last_available_confirmed = row["last_available_confirmed"]
                    last_available_confirmed_per_100k_inhabitants = row[
                        "last_available_confirmed_per_100k_inhabitants"
                    ]
                    last_available_deaths = row["last_available_deaths"]
                    state = row["state"]
                    new_confirmed = row["new_confirmed"]
                    new_deaths = row["new_deaths"]
                    csv_write.writerow(
                        [
                            city,
                            city_ibge_code,
                            date,
                            last_available_confirmed,
                            last_available_confirmed_per_100k_inhabitants,
                            last_available_deaths,
                            state,
                            new_confirmed,
                            new_deaths,
                        ]
                    )

        buscaDados(filters)

    # criando o dataset para as  cidades de redenção, Acarape e São Francisco do Conde
    with open(
        "data/df_dados_acumulados.csv", "w", newline="", encoding="utf-8"
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

        codigosIBG_CE = [
            2309458,
            2301950,
            2300150,
            2311603,
            2310100,
            2301208,
            2302107,
            2305100,
            2302909,
            2309102,
            2306504,
        ]

        codigosIBG_BA = [
            2929206,
            2933208,
            2916104,
            2919926,
            2906501,
            2930709,
            2905701,
            2910057,
            2927408,
            2919207,
            2929503,
            2921005,
            2925204,
        ]

        # pegando os dados acumulados das cidades do Ceará
        filters_CE_acumulados = {"state": "CE", "is_last": True}
        data_CE_acumlados = api.data(dataset_slug, table_name, filters_CE_acumulados)
        logging.info("Coletando os dados acumulados do Ceará")
        for row in data_CE_acumlados:
            for cod in codigosIBG_CE:
                if row["city_ibge_code"] == cod:
                    city = row["city"]
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

        # pegando os dados acumulados das cidades da Bahia
        filters_Baiha = {"state": "BA", "is_last": True}
        data_BA = api.data(dataset_slug, table_name, filters_Baiha)
        logging.info("Coletando os dados acumulados da Bahia")
        for row in data_BA:
            for cod in codigosIBG_BA:
                if row["city_ibge_code"] == cod:
                    city = row["city"]
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
    logging.info("Dados coletados!")


if __name__ == "__main__":
    main(sys.argv[1])
