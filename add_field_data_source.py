import csv

new_data = []

with open("./data/unclassified_all.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for index, row in enumerate(csv_reader):
        if row["host"] == "155.69.181.12":
            data_from = "reddit"
        else:
            data_from = "twitter"

        try:
            score = int(row["score"].replace(",", ""))
        except:
            score = 0

        new_data.append({
            "body": row["body"],
            "company": row["company"],
            "created_utc": row["created_utc"].replace(",", ""),
            "score": score,
            "data_type": "unclassified",
            "data_from": data_from
        })

with open("./data/unclassified_all_with_data_from.csv", 'w') as csv_file:
    csv_columns = [
        "body", "company", "created_utc", "score", "data_type", "data_from"
    ]

    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for data in new_data:
        writer.writerow(data)
