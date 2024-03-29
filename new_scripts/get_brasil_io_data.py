from packages.generate_csv_file import write_csv_file, get_last_update_date
from packages.api import url
import requests
import csv
import sys
import os
import logging


logging.basicConfig(level=logging.DEBUG)

payload = [
    {"state": "CE", "is_last": False, "city": "Acarape"},
    {"state": "CE", "is_last": False, "city": "Redenção"},
    {"state": "BA", "is_last": False, "city": "São Francisco do Conde"},
]

directory = "./data"

if not os.path.exists(directory):
    os.makedirs(directory)


def main(api_key):
    headers = {"authorization": f"Token {api_key}"}

    columns = [
        "city",
        "city_ibge_code",
        "date",
        "last_available_confirmed",
        "last_available_confirmed_per_100k_inhabitants",
        "last_available_deaths",
        "new_confirmed",
        "new_deaths",
    ]

    last_dates = []

    with open(f"{directory}/df_cidades_campi.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(columns)
        logging.info("Iniciando a coleta de dados")
        for filter in payload:
            logging.info(f" coletando dados de {filter['city']}")
            res = requests.get(url, headers=headers, params=filter)
            data = res.json()
            data = data["results"]
            write_csv_file(csv_write=csv_write, data=data, columns=columns)
            last_dates.append(get_last_update_date(data=data))
        logging.info("Dados coletados")

    with open(f"{directory}/last_update_dates.csv", "w", encoding="utf-8") as file:
        csv_file_date = csv.writer(file)
        csv_file_date.writerow(["city", "last_update_date"])

        for item in last_dates:
            csv_file_date.writerow([item["city"], item["date"]])


if __name__ == "__main__":
    main(sys.argv[1])
