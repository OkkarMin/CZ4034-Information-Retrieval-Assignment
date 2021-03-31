from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Python
from diagrams.firebase.develop import Firestore
from diagrams.programming.framework import React
from diagrams.onprem.client import User, Users
from diagrams.elastic.elasticsearch import Elasticsearch, Logstash, Kibana
from diagrams.elastic.enterprisesearch import AppSearch

with Diagram('Information Retrieval System', show=True):
    with Cluster('Obtaining Data'):
        twitter_crawler = Python('twitter-api')
        python_crawler = Python('reddit-api')
        crawlers = [twitter_crawler, python_crawler]

    with Cluster('Scrubbing Data'):
        scrub_data = Python('scrub/clean data')

    with Cluster('Exploring Data'):
        with Cluster('Datastore'):
            unlabelled_firestore = Firestore('un-labelled')
            labelled_firestore = Firestore('labelled')

        with Cluster('Labelling web-app'):
            labeller_web_app = React('labeller.irgroup13.ml')
            labellers = Users('labellers')

        with Cluster('ELK Stack (irgroup13.ml)'):
            elasticsearch = Elasticsearch('elasticsearch')
            logstash_unclassified = Logstash('unclassified data')
            logstash_classified = Logstash('classified data')
            kibana = Kibana('kibana')

    with Cluster('Modelling Data'):
        with Cluster('Pre-processing data'):
            pre_processing_data = Python('pre-processing data')

        with Cluster('Training classifier'):
            classifier = Python('classifier')

    with Cluster('Interpreting Data'):
        pre_processing_data_interprete = Python('pre-processing data')
        classifier_interprete = Python('classifier')
        appsearch = AppSearch('appsearch')

        with Cluster('Webapp search engine'):
            websearch_ui = React('websearch-ui')
            query_user = User('User')

        crawlers >> scrub_data >> unlabelled_firestore
        unlabelled_firestore >> labeller_web_app
        labellers >> labeller_web_app >> labelled_firestore
        scrub_data >> logstash_unclassified >> elasticsearch >> kibana
        logstash_classified >> elasticsearch
        labelled_firestore >> pre_processing_data >> classifier
        scrub_data >> pre_processing_data_interprete >> classifier_interprete >> logstash_classified
        query_user >> Edge(label='query') >> websearch_ui << appsearch
        elasticsearch >> appsearch
