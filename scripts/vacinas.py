import requests
import json

url = "https://imunizacao-es.saude.gov.br/_search"
#  r = requests.get(url, auth=HTTPBasicAuth('imunizacao_public', 'qlto5t&7r_@+#Tlstigi'))

payload = json.dumps({"size": 10000})
headers = {
    "Authorization": "Basic aW11bml6YWNhb19wdWJsaWM6cWx0bzV0JjdyX0ArI1Rsc3RpZ2k=",
    "Content-Type": "application/json",
    "Cookie": "ELASTIC-PROD=1618079452.839.9136.791476",
}

response = requests.request("POST", url, headers=headers, data=payload)

vacina = response.json()
df_vacinas = vacina["hits"]["hits"]

for row in df_vacinas:
    if row["_source"]["paciente_endereco_nmMunicipio"] == "FORTALEZA":
        print(
            row["_id"],
            row["_source"]["vacina_descricao_dose"],
            row["_source"]["paciente_endereco_nmMunicipio"],
        )
