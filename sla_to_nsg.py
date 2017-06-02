import requests
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

client = Elasticsearch(['192.168.0.24:9200'])

start = datetime.now() - timedelta(hours=24)
end = datetime.now()

start = int(start.strftime("%s")) * 1000
end  = int(end.strftime("%s")) * 1000


def stat():
    response = client.search(
        index="nuage_dpi_slastats",
        body={
         "query":{
            "bool":{
                "must":[
                {
                    "range":{
                    "timestamp":{
                        "gte":"now-24h",
                        "lte":"now",
                        "format":"epoch_millis"
                    }
                    }
                }
                ]
            }
            },
           "aggs": {
            "11": {
                "filters": {
                "filters": {
                    "DestinationNSG": {
                    "query": {
                        "term": {
                        "DestinationNSG": "default"
                        }
                    }
                    }
                }
                },
                "aggs": {
                "ts": {
                    "terms": {
                    "field": "timestamp",
                    "size": 10,
                    "order": {
                        "_count": "desc"
                    }
                    },
                    "aggs": {
                    "SourceNSG": {
                        "terms": {
                        "field": "SourceNSG",
                        "size": 10,
                        "order": {
                            "_count": "desc"
                        }
                        },
                        "aggs": {
                        "Application": {
                            "terms": {
                            "field": "Application",
                            "size": 10,
                            "order": {
                                "_count": "desc"
                            }
                            },
                            "aggs": {
                            "APMGroup": {
                                "terms": {
                                "field": "APMGroup",
                                "size": 10,
                                "order": {
                                    "_count": "desc"
                                }
                                },
                                "aggs": {
                                "ViolationType": {
                                    "terms": {
                                    "field": "ViolationType",
                                    "size": 10,
                                    "order": {
                                        "_count": "desc"
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
            }
            }
    }
    )
    return response
