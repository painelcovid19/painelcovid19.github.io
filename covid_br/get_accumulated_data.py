import pandas as pd


df_cases = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv")

codigosIBG_acum = [
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


def get_acumulated_data(ibge_codes):
    datas = []
    for cod in ibge_codes:
        df_row = df_cases[df_cases["ibgeID"] == cod]
        datas.append(df_row)
    return datas

datas = get_acumulated_data(codigosIBG_acum)

acumulated_data = pd.concat(datas)

columns = ["city", "ibgeID", "date", "totalCases","deaths_per_100k_inhabitants", "totalCases_per_100k_inhabitants", "deaths", "newCases", "newDeaths"]
new_columns =["city", "city_ibge_code", "date", "last_available_confirmed","last_available_deaths_per_100k_inhabitants", "last_available_confirmed_per_100k_inhabitants", "last_available_deaths", "new_confirmed", "new_deaths"]

acumulated_data = acumulated_data[columns]

acumulated_data.columns = new_columns


acumulated_data.reset_index(drop=True, inplace=True)

acumulated_data.head()

acumulated_data = acumulated_data.sort_values(by="city", ignore_index=True)

acumulated_data.to_csv("./data/df_dados_acumulados.csv", index=False)

