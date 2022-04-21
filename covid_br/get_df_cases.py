import pandas as pd

df_cases = pd.read_csv("covid_br/cases-brazil-cities-time.csv")

columns = [
    "city",
     "ibgeID", 
     "date", 
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

df_Acarape = df_campis[df_campis["city"] == "Acarape/CE"].sort_values(by="date", ascending=False)
df_Redencao = df_campis[df_campis["city"] == "Redenção/CE"].sort_values(by="date", ascending=False)
df_SFC = df_campis[df_campis["city"] == "São Francisco do Conde/BA"].sort_values(by="date", ascending=False)


df_campis = pd.concat([df_Acarape, df_Redencao, df_SFC])


df_campis.reset_index(inplace=True)

df_campis.drop("index", axis=1, inplace=True)

df_campis.to_csv("data/df_cidades_campi.csv", index=False)

