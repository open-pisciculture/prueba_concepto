#!/usr/bin/python3

import time
import numpy as np
# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
# Connect to the elastic cluster
# es=Elasticsearch([{'host':'192.168.0.7','port':5601}])
es = Elasticsearch(['https://search-piscicultura-kk4yptlngv2m7tdt4qz54jcbum.us-east-2.es.amazonaws.com'])

current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

doc={
    "first_name":"alejo",
    "last_name":"arias",
    "temperature": 10 * np.sin(2*np.pi * time.time()/40 ),
    "interests": ['sports','music'],
    "@timestamp": current_timestamp
}

# time_length = 30
# t0 = time.time()
num_docs = 50
doc_i = 0
# while time.time() - t0 < time_length:
while doc_i < num_docs:
    current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    doc['@timestamp'] = current_timestamp
    #Now let's store this document in Elasticsearch
    res = es.index(index='test',doc_type='guy_temp',body=doc)
    print("Posted doc", doc_i, current_timestamp, "\n")
    doc_i += 1
    time.sleep(1)