from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch()

for doc_id in range(2,11):
    name = 'doc_%s' % doc_id
    es.create(index="test", doc_type="articles", id=doc_id, body={"timestamp": datetime.now(), 'content': name })


def get_doc():
    res = es.search(index="test", doc_type="articles", body={"query": {"match": {"content": "fox"}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))

