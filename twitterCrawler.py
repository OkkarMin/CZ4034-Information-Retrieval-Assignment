#TODO  rate limit handling.
#refer to https://towardsdatascience.com/twitter-data-collection-tutorial-using-python-3267d7cfa93e
import requests
import os
import json
import configparser


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(nameTag, maxResults):
    query = "{} -is:retweet lang:en".format(nameTag)
    #query = "to:{} -is:retweet lang:en".format(nameTag)
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
    topsecret = config["secrets"]
    bearer_token = topsecret[
        "bearerToken"]  # bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)

    accountsList = [
        "Apple", "Microsoft", "Amazon", "Google", "Facebook", "riotgames",
        "Samsung", "SamsungMobile", "nvidia", "NVIDIAGeForce", "Adobe",
        "Photoshop", "Lightroom", "creativecloud", "AdobeCare", "salesforce"
    ]
    nameTag = "tableaupublic"
    firstRun = True
    ntoken = "0"
    json_response = {}
    url = create_url("to:" + nameTag,
                     100)  #remove the "to:" to search for hashtags instead
    numResults = 0
    numPages = 10
    for i in range(numPages):
        if (firstRun):
            nextUrl = url
            firstRun = False
        else:
            ntoken = json_response["meta"]["next_token"]
            nextUrl = url + '&next_token=' + ntoken

        json_response = connect_to_endpoint(nextUrl, headers)
        with open('{}Data{}.json'.format(nameTag, i), 'w') as f:
            json.dump(json_response, f)

        metaPart = json_response["meta"]
        numResults += int(metaPart["result_count"])
        if ("next_token" not in metaPart):
            break
        else:
            ntoken = metaPart["next_token"]

    print("Total No. Results (Max 1000): " + str(numResults) + " for #" +
          nameTag)


if __name__ == "__main__":
    main()
