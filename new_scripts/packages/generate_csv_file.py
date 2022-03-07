def get_columns(data, columns):
    list_of_columns = []
    for item in columns:
        list_of_columns.append(data[item])
    
    return list_of_columns

def write_csv_file(csv_write, data:None, columns:list):
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

