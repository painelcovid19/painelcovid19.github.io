from urllib import response
import requests
from packages.api import url, getYesterdaysDate
from packages.ibge_codes import codigosIBG_CE, codigosIBG_BA
import logging
import sys
import csv
import os

logging.basicConfig(level=logging.DEBUG)


date = getYesterdaysDate()
payload = {"state": "CE", "had_cases": True, "date": "{}".format(date)}

payload_baiha = {"state": "BA", "had_cases": True, "date": "{}".format(date)}

columns = [
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

directory = "./data"

if not os.path.exists(directory):
    os.makedirs(directory)


def main(api_key: str):

    headers = {"authorization": f"Token {api_key}"}

    response = requests.get(url, headers=headers, params=payload)

    data = response.json()

    data = data["results"]

    with open(
        f"{directory}/df_dados_macro_regioes_ceara.csv", "w", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)

        for row in data:
            for cod in codigosIBG_CE:
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
                    csv_writer.writerow(
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

    # coletando os dados da Baiha

    response_baiha = requests.get(url, headers=headers, params=payload_baiha)

    data_baiha = response_baiha.json()

    data_baiha = data_baiha["results"]

    with open(
        f"{directory}/df_dados_macro_regioes_bahia.csv", "w", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)

        for row in data_baiha:
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
                    csv_writer.writerow(
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


if __name__ == "__main__":
    main(sys.argv[1])
