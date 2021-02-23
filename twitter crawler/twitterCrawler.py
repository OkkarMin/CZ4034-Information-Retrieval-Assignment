#TODO  rate limit handling.
#refer to https://towardsdatascience.com/twitter-data-collection-tutorial-using-python-3267d7cfa93e
import requests
import os
import json
import configparser


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, maxResults):
    query = "{} -is:retweet lang:en".format(keyword)
    tweet_fields = "tweet.fields=author_id,public_metrics,created_at"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, maxResults)

    return url


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def start_companies_crawls(company_files_dict, directory_write_data, headers):
    for company in company_files_dict.keys():
        company_data = {"data": []}
        for keyword in company_files_dict[company]:
            print("Crawling {} for [{}]...".format(keyword, company))
            current_data = crawlKeyword(keyword, headers)
            company_data["data"].extend(current_data)
        print("-" * 30)
        print("No. Records Crawled for " + company + " is " +
              str(len(company_data["data"])))
        with open('{}{}Data.json'.format(directory_write_data, company),
                  'w') as f:
            json.dump(company_data, f)


def crawlKeyword(keyword, headers):
    first_flag = True
    next_token = "0"
    json_response = {}
    max_results = 100  #per call(page)
    num_pages = 10
    data_collect = []  #collects the pages of data crawled into a list
    url = create_url(
        "to:" + keyword,
        max_results)  #remove the "to:" to search for hashtags instead

    for i in range(num_pages):
        if (first_flag):
            next_url = url
            first_flag = False
        else:
            next_token = json_response["meta"]["next_token"]
            next_url = url + '&next_token=' + next_token

        try:
            json_response = connect_to_endpoint(next_url, headers)
        except requests.exceptions.RequestException as e:
            print("crawlKeyword ERROR!")

        meta_part = json_response["meta"]
        data_collect.extend(json_response["data"])

        if ("next_token" not in meta_part):
            break
        else:
            next_token = meta_part["next_token"]

    return data_collect


def main():
    #fill in the FULL paths before running!
    directory_write_data = "yourpath/twitter stuff/TECH_DATA_2/"
    directory_secrets = "yourpath/twitter stuff/"  #contains twitterConfig.ini

    #read in Twitter API token
    config = configparser.ConfigParser()
    config.read(directory_secrets + 'twitterConfig.ini')
    secrets = config["secrets"]
    bearer_token = secrets["bearerToken"]
    headers = create_headers(bearer_token)

    #keywords_list = ["Apple","Microsoft","Amazon","Google", "Facebook","riotgames","Samsung","SamsungMobile","nvidia","NVIDIAGeForce","Adobe", "Photoshop","Lightroom","creativecloud","AdobeCare","salesforce", "tableau","tableauPublic","SlackHQ","heroku","MuleSoft","marketingcloud","asksalesforce","herokustatus"]
    #keywords_dict = {"Apple":10,"Microsoft":10,"Amazon":10,"Google":10, "Facebook":10,"riotgames":10,"Samsung":4,"SamsungMobile":10,"nvidia":1,"NVIDIAGeForce":10,"Adobe":2, "Photoshop":5,"Lightroom":2,"creativecloud":1,"AdobeCare":5,"salesforce":2, "tableau":1,"tableauPublic":1,"SlackHQ":3,"MuleSoft":1,"heroku":1,"marketingcloud":2,"asksalesforce":1,"herokustatus":1}

    #1.1. use this dict for actual crawls
    #company_files_dict = {"apple":["Apple"],"microsoft":["Microsoft"],"amazon":["Amazon"],"google":["Google"],"facebook":["Facebook"],"tencent":["riotgames"],"samsung":["Samsung","SamsungMobile"],"nvidia":["nvidia","NVIDIAGeForce"],"adobe":["Adobe","Photoshop","Lightroom","creativecloud","AdobeCare"],"salesforce":["salesforce","tableau","tableauPublic","SlackHQ","MuleSoft","heroku","marketingcloud","asksalesforce","herokustatus"]}

    #1.2. use this minimal dict for test crawls
    #company_files_dict = {"salesforce":["tableau","salesforce"],"adobe":["creativecloud"]}

    #1.3.uncomment this to start crawling all keywords from the company_file_dict, this saves the data into the path provided
    #start_companies_crawls(company_files_dict,directory_write_data,headers)


if __name__ == "__main__":
    main()
