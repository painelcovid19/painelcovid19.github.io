from datetime import datetime, timedelta


base_url = "https://api.brasil.io/v1"
dataset = "covid19"
table_name = "caso_full"
url = f"{base_url}/dataset/{dataset}/{table_name}/data"
def getYesterdaysDate():
    date = datetime.strftime(datetime.now() - timedelta(2), "%Y-%m-%d")

    return date