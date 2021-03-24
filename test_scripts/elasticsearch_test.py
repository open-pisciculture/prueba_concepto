#!/usr/bin/python3

import time
import numpy as np
from elasticsearch import Elasticsearch 
import pandas as pd

def initialize():
    global es, doc, not_published_docs
    # Connect to the elastic cluster
    es = Elasticsearch(['https://search-pisciculture-uwdladrbcgs5v53fetxiv7cxu4.us-east-2.es.amazonaws.com/'])

    current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    doc={
        "first_name":"alejandro",
        "last_name":"arias",
        "temperature": 20 * np.sin(2*np.pi * time.time()/40 ),
        "@timestamp": current_timestamp
    }

    not_published_docs = []

def publish_doc_es(key = "default", value = None, time_stamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())):
    global es, doc
    doc[key] = value
    doc["@timestamp"] = time_stamp
    #Now let's store this document in Elasticsearch
    res = es.index(index='test',doc_type='guy_temp',body=doc)
    return res


# time_length = 120
# t0 = time.time()
# num_docs = 50
# doc_i = 0


if __name__ == '__main__':
    # while time.time() - t0 < time_length:
    # while doc_i < num_docs:
    while True:
        try:
            initialize()
            valor_temp = 10 * np.sin( 2*np.pi * time.time()/1000 )
            current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

            res = publish_doc_es(key = "temperature", value = valor_temp, time_stamp = current_timestamp)

            print(res)
            print("Posted doc", current_timestamp, "\n")
            doc_i += 1
            time.sleep(1)
        except KeyboardInterrupt:
            if len(not_published_docs) > 0:
                not_published_df = pd.DataFrame(not_published_docs)
                not_published_df.to_csv('files_not_published'+current_timestamp[:16]+'.csv', index=False, header=False)

            break
        except:
            not_published_docs.append(doc)
