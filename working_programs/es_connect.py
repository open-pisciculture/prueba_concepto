#!/usr/bin/python3

import time
import numpy as np
from elasticsearch import Elasticsearch 
import pandas as pd

global es, doc, not_published_docs
es = None
doc = {}
not_published_docs = []

def initialize_es_cluster():
    '''
        This function connects with ElasticSearch Cluster in AWS
        Defines default document (name, last_name, temperature, current_timestamp)
    '''
    global es, doc, not_published_docs
    # Connect to the elastic cluster
    es = Elasticsearch(['https://search-pisciculture-uwdladrbcgs5v53fetxiv7cxu4.us-east-2.es.amazonaws.com/'])

    current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) # Timestamp in UTC time

    doc={
        "first_name":"alejandro",
        "last_name":"arias",
        "temperature": 20 * np.sin(2*np.pi * time.time()/40 ),
        "@timestamp": current_timestamp
    }

    not_published_docs = []

def publish_doc_es(dict = {'default': None}, time_stamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())):
    global es, doc
    for key in dict:
        doc[key] = dict[key]
    doc["@timestamp"] = time_stamp
    #Now let's store this document in Elasticsearch
    res = es.index(index='test_2',doc_type='sensor_values',body=doc)
    return res


if __name__ == '__main__':
    while True:
        initialize_es_cluster()
        try:
            initialize_es_cluster()
            value_temp = 35 * np.sin( 2*np.pi * time.time()/1000 )
            value_pH = 7 * np.sin( 2*np.pi * time.time()/1000 ) + 7
            value_DO = 1 * np.sin( 2*np.pi * time.time()/3000 )
            current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

            res = publish_doc_es(dict = {"temperature": value_temp, "pH": value_pH, "DO": value_DO}, time_stamp = current_timestamp)
            print("------------------- Published doc to ES -------------------")
            print(f"Type: {res['_type']} with ID: {res['_id']} \n")
            time.sleep(1)
        except KeyboardInterrupt:
            if len(not_published_docs) > 0:
                not_published_df = pd.DataFrame(not_published_docs)
                not_published_df.to_csv('files_not_published'+current_timestamp[:16]+'.csv', index=False, header=False)

            break
        except Exception as e:
            print("Couldn't publish because:", e, "\n Will save document on a list \n\n")
            not_published_docs.append(doc)
            time.sleep(5)
