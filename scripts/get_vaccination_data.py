from elasticsearch import Elasticsearch, client
from elasticsearch_dsl import Search
from tqdm import tqdm
import csv

locations = {
    "Redenção": ["REDENCAO", "CE"],
    "Acarape": ["ACARAPE", "CE"],
    "SFC": ["SAO FRANCISCO DO CONDE", "BA"],
}

client = Elasticsearch(
    "https://imunizacao-es.saude.gov.br/",
    headers={
        "Authorization": "Basic aW11bml6YWNhb19wdWJsaWM6cWx0bzV0JjdyX0ArI1Rsc3RpZ2k=",
        "Content-Type": "application/json",
        "Cookie": "ELASTIC-PROD=1618079452.839.9136.791476",
    },
)

for key in locations.keys():
    city, state = locations[key]

    print(f"Starting to retrieve vaccination data for {city} ({state})...")

    s = (
        Search(using=client)
        .query("match_phrase", paciente_endereco_nmMunicipio=city)
        .query("match_phrase", paciente_endereco_uf=state)
    )

    print("Query = ", s.to_dict())

    total_hits = s.count()
    print("Total hits = ", total_hits)

    scan = s.scan()

    data = []
    for hit in tqdm(s.scan(), total=total_hits):
        data.append(
            {
                "vacina_dataAplicacao": hit.vacina_dataAplicacao,
                "vacina_descricao_dose": hit.vacina_descricao_dose,
                "vacina_fabricante_nome": hit.vacina_fabricante_nome,
                "vacina_nome": hit.vacina_nome,
                # "paciente_idade": hit.paciente_idade,
                # "paciente_dataNascimento": hit.paciente_dataNascimento,
            }
        )

    print("Saving CSV...")
    keys = data[0].keys()
    with open(
        f"data/vaccines-{city}-{state}.csv".lower().replace(" ", "-"),
        "w",
        newline="",
        encoding="utf-8",
    ) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
