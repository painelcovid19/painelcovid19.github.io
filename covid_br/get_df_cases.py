import pandas as pd
import os
import csv
from packages.utils import get_last_update_date, rename_city

df_cases = pd.read_csv("https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz?raw=true", compression='gzip')

columns = [
    "city",
     "ibgeID", 
     "date",
     "state", 
     "totalCases",
      "totalCases_per_100k_inhabitants", 
      "deaths", 
      "newCases", 
      "newDeaths"
      ]

df_filter = (df_cases["city"] == "Acarape/CE") | (df_cases["city"] == "Redenção/CE") | (df_cases["city"] == "São Francisco do Conde/BA")

df_campis = df_cases[df_filter][columns]

df_campis.columns = ["city", "city_ibge_code", "date", "state", "last_available_confirmed", "last_available_confirmed_per_100k_inhabitants", "last_available_deaths", "new_confirmed", "new_deaths"]

df_campis = df_campis.sort_values(by="city")
df_campis["city"] = df_campis["city"].apply(rename_city)

df_Acarape = df_campis[df_campis["city"] == "Acarape"].sort_values(by="date", ascending=False)
df_Redencao = df_campis[df_campis["city"] == "Redenção"].sort_values(by="date", ascending=False)
df_SFC = df_campis[df_campis["city"] == "São Francisco do Conde"].sort_values(by="date", ascending=False)

df_campis = pd.concat([df_Acarape, df_Redencao, df_SFC])


last_updated_date = []
last_updated_date.append(get_last_update_date(df_Acarape))
last_updated_date.append(get_last_update_date(df_Redencao))
last_updated_date.append(get_last_update_date(df_SFC))

df_campis.reset_index(inplace=True)

df_campis.drop("index", axis=1, inplace=True)

directory = "./data"

if not os.path.exists(directory):
    os.makedirs(directory)

df_campis.to_csv(f"{directory}/df_cidades_campi.csv", index=False)

with open(f"{directory}/last_update_dates.csv", "w", encoding="utf-8") as csv_file:
    csv_writer= csv.writer(csv_file)
    csv_writer.writerow(["city", "dates"])
    for row in last_updated_date:
        city = row["city"]
        date = row["date"]
        csv_writer.writerow([
            city,
            date
        ])