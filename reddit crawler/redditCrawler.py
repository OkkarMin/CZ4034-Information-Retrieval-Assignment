import praw
import sys, getopt
import json
from types import SimpleNamespace
import emoji
import requests
import configparser

def post_to_logstash(data_in_json):
    logstash_http_endpoint = "http://irgroup13.ml:5151"
    requests.post(logstash_http_endpoint, json=data_in_json)

def api():
    
    comment_field = ('body', 'score', 'created_utc')

    config = configparser.ConfigParser()
    config.read('redditConfig.ini')
    reddit = praw.Reddit(client_id = config['REDDIT']["client_id"],
                         client_secret = config['REDDIT']["client_secret"],
                         username = config['REDDIT']["username"],
                         password = config['REDDIT']["password"],
                         user_agent = config['REDDIT']["user_agent"])

    
    company_sub_dict = {"apple":"Apple","microsoft":"Microsoft","amazon":"Amazon","google":"Google","facebook":"Facebook","tencent":"riotgames","samsung":"Samsung","nvidia":"nvidia","adobe":"Adobe"}
    subreddit_list = list(company_sub_dict.values()) 
    company_list = list(company_sub_dict.keys()) 
    
    for i in range(9):
        
        subreddit = reddit.subreddit(subreddit_list[i]) 
        print("printing..."+str(subreddit))
        sub = subreddit.new(limit=1500)
        with open('results.py', 'w+') as fout: 
            count = 0

            for submission in sub:
                
                for comment1 in submission.comments.list(): 
                    
                    to_dict = vars(comment1)

                    if(to_dict['id'] != '_' and to_dict['body'] != '[deleted]'):
                        sub_dict = {field:to_dict[field] for field in comment_field}
                        sub_dict["company"] = company_list[i]

                        # Data cleaning 
                        body = sub_dict["body"]
                        body = body.replace("\u2019","'")
                        body = emoji.demojize(body).replace(":"," ")
                        body = body.encode('ascii', errors='ignore').decode('utf-8')
                        body = body.replace('\n','')
                        body = body.strip()
                        body= " ".join(body.split())
                        sub_dict["body"] = body
                        time = sub_dict["created_utc"]
                        time = int(time)
                        sub_dict["created_utc"] = time
                        json_data = json.dumps(sub_dict, indent=4)
                        fout.write(json_data)

                        # Push to logstash
                        post_to_logstash(sub_dict) 
                        count = count+1
                        
                    if (count == 1000): 
                        break
                if (count == 1000): 
                        break
 
        fout.close()
        
if __name__ == "__main__":
    api()
