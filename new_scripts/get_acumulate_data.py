from packages.generate_csv_file import write_csv_file, get_last_update_date, get_camulated_data
from packages.ibge_codes import codigosIBG_acum
from packages.api import getYesterdaysDate
from packages.api import url
import requests
import sys
import csv
import os


filters = [
    {
        "state": "CE",
        "had_cases": True,
        "date": "{}".format(getYesterdaysDate()),
    },
    {
        "state": "BA",
        "had_cases": True,
        "date": "{}".format(getYesterdaysDate()),
    },
]


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

last_dates = []

directory = "./data"

if not os.path.exists(directory):
    os.makedirs(directory)


def main(api_key):
    headers = {"authorization": f"Token {api_key}"}

    response_CE = requests.get(url, headers=headers, params=filters[0])
    response_BA = requests.get(url, headers=headers, params=filters[1])

    data_CE = response_CE.json()

    data_CE = data_CE["results"]

    data_BA = response_BA.json()
    data_BA = data_BA["results"]

    All_datas = data_CE + data_BA

    with open(
        f"{directory}/df_dados_acumulados.csv", "w", newline="", encoding="utf-8"
    ) as ac_file:
        ac_file_write = csv.writer(ac_file)
        ac_file_write.writerow(columns)
        get_camulated_data(data=All_datas, codigos_IBG=codigosIBG_acum, opened_file=ac_file_write)


if __name__ == "__main__":
    main(sys.argv[1])
