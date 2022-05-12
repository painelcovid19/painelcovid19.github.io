import logging

logging.basicConfig(level=logging.DEBUG)

def get_last_update_date(data):
    last_updates = {}
    for index, row in enumerate(data["new_confirmed"]):
        if row >= 1:
            last_updates["city"] = data["city"].loc[0]
            last_updates["date"] = data.loc[index, "date"]
            break
    return last_updates

def get_datas(ibge_codes_list, df_of_cases):
    datas = []
    for cod in ibge_codes_list:
        df_row = df_of_cases[df_of_cases["ibgeID"] == cod]
        datas.append(df_row)
    return datas

def rename_city(city):
    city_name, uf = city.split("/")
    city = city_name
    return city

columns = ["city", "ibgeID", "date","state", "totalCases","deaths_per_100k_inhabitants", "totalCases_per_100k_inhabitants", "deaths", "newCases", "newDeaths"]
new_columns =["city", "city_ibge_code", "date", "state", "last_available_confirmed","last_available_deaths_per_100k_inhabitants", "last_available_confirmed_per_100k_inhabitants", "last_available_deaths", "new_confirmed", "new_deaths"]