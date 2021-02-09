
#cleans up the crawled data
import emoji
import json 
from datetime import datetime
import string


#Converts iso 8601 datetime to epoch datetime.
def iso_to_epoch(iso_str):
    date_object = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%f")
    epoch_int = round(date_object.timestamp(),0)
    return int(epoch_int)

#Remove mentions, convert emoji to descriptions, remove extra \u and whitespaces, remove URLs
def process_body(body_str):
    #remove all mentions 
    body_str = "".join([" " if "@" in word else word + " " for word in body_str.split()])

    #replace '
    body_str = body_str.replace("\u2019","'")

    #translate emoji characters into descriptions
    body_str = emoji.demojize(body_str).replace(":"," ")

    #remove URLs
    body_str = "".join([" " if "https" in word or "//t.co" in word else word + " " for word in body_str.split()])

    #remove excess whitespace
    body_str = body_str.strip()
    body_str = " ".join(body_str.split())
    
    #remove any other \u from the body
    body_str = body_str.encode('ascii', errors='ignore').decode('utf-8')

    return body_str


f = open('creativecloudData0.json',)
#f = open('testData.json',)
fDict = json.load(f) 
company = "adobe"

new_dict = {}
new_dict["data"] = []

#process raw data
for entry in fDict["data"]:
    new_entry = {}
    new_entry["body"] = process_body(entry["text"])
    new_entry["score"] = sum(entry['public_metrics'].values())
    new_entry["created_utc"] = iso_to_epoch(entry["created_at"][:-1])
    new_entry["company"] = company
    new_dict["data"].append(new_entry)
    
#save formatted data into new file
with open('cleanedData.json', 'w') as p:
            json.dump(new_dict,p)

f.close()



