import requests
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

client = Elasticsearch(['192.168.0.24:9200'])

start = datetime.now() - timedelta(hours=24)
end = datetime.now()

start = int(start.strftime("%s")) * 1000
end  = int(end.strftime("%s")) * 1000



response = client.search(
    index="nuage_dpi_flowstats-2017-05-13",
    body={ "sort":[ { "timestamp":{ "order":"desc" } } ], "query":{ "bool":{ "should":[ { "bool":{ "must":[ { "term":{ "SourceNSG":"nsg-branch1" } }, { "term":{ "DestinationNSG":"nsg-branch2" } }, ] } } ] } } }
)

for hit in response['hits']['hits']:
    print '*' * 1000
    print hit
 


URL = 'http://192.168.0.24:9200'

print '#' * 1000
print 'DPI SLA STATS'

DPI_sla_stats= requests.get(URL  + "/nuage_dpi_slastats-2017-05-10/_search?pretty")
print DPI_sla_stats.json()

print '$' * 1000
print 'DPI FLOW STATS'

DPI_flow_stats= requests.get(URL  + "/nuage_dpi_flowstats-2017-05-10/_search?pretty")
print DPI_flow_stats.json()
