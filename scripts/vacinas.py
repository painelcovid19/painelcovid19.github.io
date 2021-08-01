import requests
import csv
import json

# url = "https://imunizacao-es.saude.gov.br/_search"
#  r = requests.get(url, auth=HTTPBasicAuth('imunizacao_public', 'qlto5t&7r_@+#Tlstigi'))

# funcão para geraro csv
def gerateCSV(df_vacinas):
        with open("data/df_dados_vacinas.csv", "a", newline="", encoding="utf-8") as csvDadosVacina:
            csvVacina = csv.writer(csvDadosVacina)
            csvVacina.writerow(
                [
                    "paciente_endereco_nmMunicipio",
                    "vacina_descricao_dose",
                    "vacina_fabricante_nome",
                    "vacina_nome",
                    "estabelecimento_uf",
                ]
            ) 

            for row in df_vacinas:
                if row["_source"]["estabelecimento_uf"] == "CE":
                    paciente_endereco_nmMunicipio = row["_source"]["paciente_endereco_nmMunicipio"]
                    vacina_descricao_dose = row["_source"]["vacina_descricao_dose"]
                    vacina_fabricante_nome = row["_source"]["vacina_fabricante_nome"]
                    vacina_nome = row["_source"]["vacina_nome"]
                    estabelecimento_uf = row["_source"]["estabelecimento_uf"]
                    csvVacina.writerow(
                        [
                            paciente_endereco_nmMunicipio,
                            vacina_descricao_dose,
                            vacina_fabricante_nome,
                            vacina_nome,
                            estabelecimento_uf,
                        ]
                    )

#  função para fazer as requisições na API
def firstRequest(body, link):
     
     url = link
     payload = json.dumps(body)
     headers = {
        "Authorization": "Basic aW11bml6YWNhb19wdWJsaWM6cWx0bzV0JjdyX0ArI1Rsc3RpZ2k=",
        "Content-Type": "application/json",
        "Cookie": "ELASTIC-PROD=1618079452.839.9136.791476",
     }

     response = requests.request("GET", url, headers=headers, data=payload)

     vacina = response.json()
     return vacina
     
body_1 =  { 
    "size": 10000,
    # "query": {
    #         # "bool": {
    #         #     "must": [
    #         #         {"match": {"paciente_endereco_nmMunicipio": "REDENCAO"}},
    #         #         {"match": {"estabelecimento_uf": "CE"}},
    #         #     ],
    #         # },
    #         # "query_string": {
    #         #     "default_field": "paciente_endereco_nmMunicipio",
    #         #     "query": "ACARAPE OR REDENCAO",
    #         # }
    #     }
    }
url_1 = "https://imunizacao-es.saude.gov.br/_search?scroll=1m"


vacina = firstRequest(body_1, url_1)
scroll_id =  vacina["_scroll_id"] 
df_vacinas = vacina["hits"]["hits"]
# gerateCSV(df_vacinas)

body_2 =  { 

    "scroll_id": f"{scroll_id}" ,
    "scroll": "1m",
    # "query": {
    #         # "bool": {
    #         #     "must": [
    #         #         {"match": {"paciente_endereco_nmMunicipio": "REDENCAO"}},
    #         #         {"match": {"estabelecimento_uf": "CE"}},
    #         #     ],
    #         # },
    #         "query_string": {
    #             "default_field": "paciente_endereco_nmMunicipio",
    #             "query": "ACARAPE OR REDENCAO",
    #         }
    #     }
    }
url_2 = "https://imunizacao-es.saude.gov.br/_search/scroll"
# vacina = firstRequest(body_1, url_1)

# with open('data/df_vacinas_01.json', 'w') as f:
#     json.dump(vacina, f)
#  csvVacina = csv.writer(csvDadosVacina)

vacina_2 = firstRequest(body_2, url_2)
df_vacinas_2 = vacina_2["hits"]["hits"]
gerateCSV(df_vacinas_2)

while (len(df_vacinas_2)!= 0):
    vacina_2 = firstRequest(body_2, url_2)
    df_vacinas_2 = vacina_2["hits"]["hits"]
    gerateCSV(df_vacinas_2)
    print(len(df_vacinas_2))


print(scroll_id)
print(len(df_vacinas_2))

# scroll_id = vacina._scroll_id
# df_vacinas = vacina["hits"]["hits"]

# print(scroll_id)



