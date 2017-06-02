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
		      "4":{
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
		            "3":{
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
		                  "Application":{
		                     "date_histogram":{
		                        "field":"timestamp",
		                        "interval":"1m"
		                     },
		                     "aggs":{
		                        "using":{
		                           "terms":{
				                        "field":"Application",
				                        "order":{
				                           "Sum of MB":"desc"
				                        }
				                     },
				                     "aggs":{
				                        "Sum of MB":{
				                           "sum":{
				                              "field":"TotalMB"
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
