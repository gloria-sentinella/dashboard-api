import json
from elasticsearch import Elasticsearch

client = Elasticsearch(['192.168.0.24:9200'])

def stat(SourceNSG,SrcUplink):
    response = client.search(
    index="nuage_dpi_slastats",
    body={
	  "query": {
	    "filtered": {
	      "query": {
	        "range" : {
	            "timestamp" : {
	                "gte":"now-24h",
		            "lte":"now",
		            "format":"epoch_millis"
	            }
	        }
	      },
	      "filter" : {
	            "bool" : {
	                "must" : [
	                    { "term" : { "SourceNSG" : "{0}".format(SourceNSG) } }, 
	                    { "term" : { "DstUplink" : "{0}".format(SrcUplink) } } 
	                ]
	            }
	        }
	    }
	  },
      "sort" : [
          {"timestamp" : {"order" : "desc"}}
      ]
	}
    )
    return response
