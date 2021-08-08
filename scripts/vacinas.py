import requests
import csv
import json

# funcão para geraro csv

csvName = ["df_vacinas_redencao","df_vacinas_acarape","df_vacinas_SFC"]

def gerateCSV(df_vacinas,file_name):
        with open(f"data/{file_name}.csv", "w", newline="", encoding="utf-8") as csvDadosVacina:
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
def request(body, url):
     payload = json.dumps(body)
     headers = {
        "Authorization": "Basic aW11bml6YWNhb19wdWJsaWM6cWx0bzV0JjdyX0ArI1Rsc3RpZ2k=",
        "Content-Type": "application/json",
        "Cookie": "ELASTIC-PROD=1618079452.839.9136.791476",
     }

     response = requests.request("POST", url, headers=headers, data=payload)
     if response.status_code != 200:
         print(response.json())
     vacina = response.json()
     return vacina

size = 10000
body_3 = {
    "size": size,
    "query": {
            "bool": {
                "must": [
                    {"match": {"paciente_endereco_coIbgeMunicipio": 2929206}},
                ],
    #         },
    #         # "query_string": {
    #         #     "default_field": "paciente_endereco_nmMunicipio",
    #         #     "query": "ACARAPE OR REDENCAO",
    #         # }
        }
    }
}

body_1 =  { 
    "size": size,
    "query": {
            "bool": {
                "must": [
                    {"match": {"paciente_endereco_nmMunicipio":{"query": "SAO FRANCISCO DO CONDE", "fuzziness": 0}}},
                    {"match": {"paciente_endereco_uf": {"query": "BA", "fuzziness": 0}}},
                ],
    #         },
    #         # "query_string": {
    #         #     "default_field": "paciente_endereco_nmMunicipio",
    #         #     "query": "ACARAPE OR REDENCAO",
    #         # }
        }
    }
}

body_2 =  { 

    "scroll_id":"" ,
    "scroll": "1m",
 }


url_1 = "https://imunizacao-es.saude.gov.br/_search?scroll=1m"
url_2 = "https://imunizacao-es.saude.gov.br/_search/scroll"

# função principal
def main(body_1, body_2, url_1, url_2, city_name, UF, file_name1, file_name2):
    # body_1["query"]["bool"]["must"][0]["match"]["paciente_endereco_nmMunicipio"] = city_name 
    # body_1["query"]["bool"]["must"][1]["match"]["paciente_endereco_uf"] = UF

    vacina = request(body_1, url_1)
    scroll_id =  vacina["_scroll_id"] 
    body_2["scroll_id"] = scroll_id 
    df_vacinas = vacina["hits"]["hits"]
    print(scroll_id )
    
    if len(df_vacinas) < size:
        print(len(df_vacinas))
        gerateCSV(df_vacinas, file_name1)
        exit()
    else:
        gerateCSV(df_vacinas, file_name1)
        while len(df_vacinas) != 0:
            print(len(df_vacinas))
            vacina_2 = request(body_2, url_2)
            df_vacinas_2 = vacina_2["hits"]["hits"]
            gerateCSV(df_vacinas_2, file_name2)
            df_vacinas = df_vacinas_2
    exit()


main(body_1,body_2,url_1,url_2, "SAO FRANCISCO DO CONDE","BA",csvName[2],"teste")
