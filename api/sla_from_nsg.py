from elasticsearch import Elasticsearch

client = Elasticsearch(['192.168.0.24:9200'])

def stat():
    response = client.search(
        index="nuage_dpi_flowstats",
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
                    "SourceNSG": {
                    "query": {
                        "term": {
                        "SourceNSG": "default"
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
                    "DestinationNSG": {
                        "terms": {
                        "field": "DestinationNSG",
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
