import logging

logging.basicConfig(level=logging.DEBUG)


def get_columns(data, columns):
    list_of_columns = []
    for item in columns:
        list_of_columns.append(data[item])

    return list_of_columns


def write_csv_file(csv_write, data: None, columns: list):
    for row in data:
        csv_write.writerow(get_columns(data=row, columns=columns))


cities = ["Acarape", "Redenção", "São Francisco do Conde"]


def get_last_update_date(data):
    last_updates = {}
    for row in data:
        if row["new_confirmed"]:
            last_updates["city"] = row["city"]
            last_updates["date"] = row["date"]
            break
    return last_updates


def get_camulated_data(data: list, codigos_IBG: list, opened_file):
    logging.info("começando a coleta dos dados")
    for row in data:
        for cod in codigos_IBG:
            if row["city_ibge_code"] == cod:
                logging.info(f"Coletando os dados de {row['city']}...")
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
                opened_file.writerow(
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
    logging.info("Dados coletados")
