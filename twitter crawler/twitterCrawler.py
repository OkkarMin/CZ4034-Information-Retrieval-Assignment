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


def main():
    #read in Twitter API token
    config = configparser.ConfigParser()
    config.read('twitterConfig.ini')
    secrets = config["secrets"]
    bearer_token = secrets[
        "bearerToken"]  # bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)

    keywords_list = [
        "Apple", "Microsoft", "Amazon", "Google", "Facebook", "riotgames",
        "Samsung", "SamsungMobile", "nvidia", "NVIDIAGeForce", "Adobe",
        "Photoshop", "Lightroom", "creativecloud", "AdobeCare", "salesforce",
        "tableau", "tableauPublic", "SlackHQ", "heroku", "MuleSoft",
        "marketingcloud", "asksalesforce", "herokustatus"
    ]
    keyword = keywords_list[-1]
    first_flag = True
    next_token = "0"
    json_response = {}
    num_results = 0
    max_results = 100  #per call(page)
    num_pages = 10
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

        json_response = connect_to_endpoint(next_url, headers)
        with open('{}Data{}.json'.format(keyword, i), 'w') as f:
            json.dump(json_response, f)

        meta_part = json_response["meta"]
        num_results += int(meta_part["result_count"])
        if ("next_token" not in meta_part):
            break
        else:
            next_token = meta_part["next_token"]

    print("Total No. Results (Max 1000): " + str(num_results) + " for #" +
          keyword)


if __name__ == "__main__":
    main()
