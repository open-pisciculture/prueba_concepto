#!/usr/bin/python3

import time
import numpy as np
from elasticsearch import Elasticsearch 
import pandas as pd
import es_connect

global es, doc, not_published_docs
es = None
doc = {}
not_published_docs = []



if __name__ == '__main__':
    while True:
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