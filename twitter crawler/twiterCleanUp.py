
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

def process_data(new_dict, data_list):
    #process raw data
    for entry in data_list:
        new_entry = {}
        new_entry["body"] = process_body(entry["text"])
        new_entry["score"] = sum(entry['public_metrics'].values())
        new_entry["created_utc"] = iso_to_epoch(entry["created_at"][:-1])
        new_entry["company"] = company
        new_dict["data"].append(new_entry)

keywords_dict = {"Apple":10,"Microsoft":10,"Amazon":10,"Google":10, "Facebook":10,"riotgames":10,"Samsung":4,"SamsungMobile":10,"nvidia":1,"NVIDIAGeForce":10,"Adobe":2, "Photoshop":5,"Lightroom":2,"creativecloud":1,"AdobeCare":5,"salesforce":2, "tableau":1,"tableauPublic":1,"SlackHQ":3,"MuleSoft":1,"heroku":1,"marketingcloud":2,"asksalesforce":1,"herokustatus":1}
company_files_dict = {"apple":["Apple"],"microsoft":["Microsoft"],"amazon":["Amazon"],"google":["Google"],"facebook":["Facebook"],"tencent":["riotgames"],"samsung":["Samsung","SamsungMobile"],"nvidia":["nvidia","NVIDIAGeForce"],"adobe":["Adobe","Photoshop","Lightroom","creativecloud","AdobeCare"],"salesforce":["salesforce","tableau","tableauPublic","SlackHQ","MuleSoft","heroku","marketingcloud","asksalesforce","herokustatus"]}

company = "salesforce"
files_list = company_files_dict[company]
company_data_list = []
new_dict = {}
new_dict["data"] = []

raw_data_directory = 'TECH_DATA/'
cleaned_data_directory = 'CLEANED_DATA/'
for k in files_list:
    for i in range(keywords_dict[k]):
        file_name ="{}Data{}.json".format(k,i)
        f = open(raw_data_directory+file_name,)
        fDict = json.load(f) 
        f.close()
        process_data(new_dict,fDict["data"])

created_file_name = company+"_cleaned.json"
print("{} entries in {} created!".format(len(new_dict["data"]),created_file_name))
with open(cleaned_data_directory + created_file_name, 'w') as p:
            json.dump(new_dict,p)







