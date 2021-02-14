import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import csv

# Use a service account
cred = credentials.Certificate("./serviceAccount.log")
firebase_admin.initialize_app(cred)
firebase = firestore.client()

# Unclassified data collection
collection = firebase.collection('unclassified')

with open("./data/all_unclassified_data_shuffled.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for index, row in enumerate(csv_reader):

        payload = {
            "dataID": index,
            "body": row["body"],
            "company": row["company"],
            "created_utc": row["created_utc"].replace(",", ""),
            "score": int(row["score"].replace(",", "")),
            "data_type": row["type"]
        }

        if 3202 <= index < 8888:
            print(payload)
            collection.document(str(index)).set(payload)
