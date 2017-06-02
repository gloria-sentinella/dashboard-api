import json
from elasticsearch import Elasticsearch

client = Elasticsearch(['192.168.0.24:9200'])

def stat(SourceNSG,SrcUplink):
    response = client.search(
	    index="nuage_dpi_flowstats",
	    body={
		   "size":0,
		   "query":{
		      "bool":{
		         "must":[
		            {
		               "range":{
		                  "timestamp":{
		                     "gte":"now-15m",
		                     "lte":"now",
		                     "format":"epoch_millis"
		                  }
		               }
		            }
		         ]
		      }
		   },
		   "aggs":{
		      "5":{
		         "filters":{
		            "filters":{
		               "SourceNSG":{
		                  "query":{
		                     "term":{
		                        "SourceNSG":"{0}".format(SourceNSG)
		                     }
		                  }
		               }
		            }
		         },
		         "aggs":{
		            "4":{
		               "filters":{
		                  "filters":{
		                     "SrcUplink":{
		                        "query":{
		                           "term":{
		                              "SrcUplink":"{0}".format(SrcUplink)
		                           }
		                        }
		                     }
		                  }
		               },
		               "aggs":{
		                  "ts":{
		                     "date_histogram":{
		                        "field":"timestamp",
		                        "interval":"1m"
		                     },
		                     "aggs":{
		                        "L7Classification":{
		                           "terms":{
		                              "field":"L7ClassEnhanced",
		                              "size":5,
		                              "order":{
		                                 "SumOf":"desc"
		                              }
		                           },
		                           "aggs":{
		                              "SumOf":{
		                                 "sum":{
		                                    "field":"TotalBytesCount"
		                                 }
		                              }
		                           }
		                        }
		                     }
		                  }
		               }
		            }
		         }
		      }
		   }
		}
	)
    return response
