import requests
import json


def post_to_logstash(data_in_json):
    logstash_http_endpoint = "http://irgroup13.ml:5151"

    requests.post(logstash_http_endpoint, json=data_in_json)


try:
    keywords_dict = {
        "Apple": 10,
        "Microsoft": 10,
        "Amazon": 10,
        "Google": 10,
        "Facebook": 10,
        "riotgames": 10,
        "Samsung": 4,
        "SamsungMobile": 10,
        "nvidia": 1,
        "NVIDIAGeForce": 10,
        "Adobe": 2,
        "Photoshop": 5,
        "Lightroom": 2,
        "creativecloud": 1,
        "AdobeCare": 5,
        "salesforce": 2,
        "tableau": 1,
        "tableauPublic": 1,
        "SlackHQ": 3,
        "MuleSoft": 1,
        "heroku": 1,
        "marketingcloud": 2,
        "asksalesforce": 1,
        "herokustatus": 1
    }
    company_files_dict = {
        "apple": ["Apple"],
        "microsoft": ["Microsoft"],
        "amazon": ["Amazon"],
        "google": ["Google"],
        "facebook": ["Facebook"],
        "tencent": ["riotgames"],
        "samsung": ["Samsung", "SamsungMobile"],
        "nvidia": ["nvidia", "NVIDIAGeForce"],
        "adobe":
        ["Adobe", "Photoshop", "Lightroom", "creativecloud", "AdobeCare"],
        "salesforce": [
            "salesforce", "tableau", "tableauPublic", "SlackHQ", "MuleSoft",
            "heroku", "marketingcloud", "asksalesforce", "herokustatus"
        ]
    }

    company = "salesforce"
    print("Sending..." + company)
    files_list = company_files_dict[company]
    companies_list = list(company_files_dict.keys())
    cleaned_data_directory = 'CLEANED_DATA/'

    file_name = "{}_cleaned.json".format(company)

    f = open(cleaned_data_directory + file_name, )
    fDict = json.load(f)
    f.close()

    for entry in fDict["data"]:
        post_to_logstash(entry)
    print("...COMPLETED!")
except Exception as e:
    print(e)
