import json
from elasticsearch import Elasticsearch

client = Elasticsearch(['192.168.0.24:9200'])

def stat(SourceNSG,SrcUplink,interval):
    response = client.search(
    index="nuage_dpi_probestats",
    body={
	  "query": {
	    "filtered": {
	      "query": {
	        "range" : {
	            "timestamp" : {
	                "gte" : "now-5m"
	            }
	        }
	      },
	      "filter" : {
	            "bool" : {
	                "must" : [
	                    { "term" : { "SourceNSG" : "{0}".format(SourceNSG) } }, 
	                    { "term" : { "SrcUplink" : "{0}".format(SrcUplink) } } 
	                ]
	            }
	        }
	    }
	  },
	  "aggs" : {
        "probes_peer_interval" : {
            "date_histogram" : {
                "field" : "timestamp",
                "interval" : "{0}".format(interval)
            },
            "aggs": {
		        "AvgJitter": {
		          "sum": {
		            "field": "AvgJitter"
		          }
		        }
		    }
        },
	    "avg_interval_payload": {
	      "avg_bucket": {
	        "buckets_path": "probes_peer_interval>AvgJitter" 
	      }
	    }
      },
      "sort" : [
          {"timestamp" : {"order" : "desc"}}
      ],
      "from" : 0, "size" : 1
	}
    )
    return json.dumps(response, indent=4, sort_keys=True) 
