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
            "aggs":{
            "4":{
                "filters":{
                "filters":{
                    "Enterprise":{
                    "query":{
                        "term":{
                        "EnterpriseName":"test_organization"
                        }
                    }
                    }
                }
                },
                "aggs":{
                "3":{
                    "filters":{
                    "filters":{
                        "SourceNSG":{
                        "query":{
                            "term":{
                            "SourceNSG":"ovs-114"
                            }
                        }
                        }
                    }
                    },
                    "aggs":{
                    "Application":{
                        "terms":{
                        "field":"Application",
                        "size":10,
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
    )
    return response
