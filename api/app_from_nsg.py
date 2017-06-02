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
            "12":{
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
                    "SumofBytes": {
                        "sum": {
                        "field": "TotalBytesCount"
                        }
                    },
                    "SumofPackets": {
                        "sum": {
                        "field": "TotalPacketsCount"
                        }
                    },
                    "APMGroup": {
                        "terms": {
                        "field": "APMGroup",
                        "size": 5,
                        "order": {
                            "SumofBytes": "desc"
                        }
                        },
                        "aggs": {
                        "SumofBytes": {
                            "sum": {
                            "field": "TotalBytesCount"
                            }
                        },
                        "SumofPackets": {
                            "sum": {
                            "field": "TotalPacketsCount"
                            }
                        },
                        "Application": {
                            "terms": {
                            "field": "Application",
                            "size": 5,
                            "order": {
                                "SumofBytes": "desc"
                            }
                            },
                            "aggs": {
                            "SumofBytes": {
                                "sum": {
                                "field": "TotalBytesCount"
                                }
                            },
                            "SumofPackets": {
                                "sum": {
                                "field": "TotalPacketsCount"
                                }
                            },
                            "L7Classification": {
                                "terms": {
                                "field": "L7ClassEnhanced",
                                "size": 5,
                                "order": {
                                    "SumofBytes": "desc"
                                }
                                },
                                "aggs": {
                                "SumofBytes": {
                                    "sum": {
                                    "field": "TotalBytesCount"
                                    }
                                },
                                "SumofPackets": {
                                    "sum": {
                                    "field": "TotalPacketsCount"
                                    }
                                },
                                "SrcVportName": {
                                    "terms": {
                                    "field": "SrcVportName",
                                    "size": 5,
                                    "order": {
                                        "SumofBytes": "desc"
                                    }
                                    },
                                    "aggs": {
                                    "SumofBytes": {
                                        "sum": {
                                        "field": "TotalBytesCount"
                                        }
                                    },
                                    "SumofPackets": {
                                        "sum": {
                                        "field": "TotalPacketsCount"
                                        }
                                    },
                                    "SrcUplink": {
                                        "terms": {
                                        "field": "SrcUplink",
                                        "size": 5,
                                        "order": {
                                            "SumofBytes": "desc"
                                        }
                                        },
                                        "aggs": {
                                        "SumofBytes": {
                                            "sum": {
                                            "field": "TotalBytesCount"
                                            }
                                        },
                                        "SumofPackets": {
                                            "sum": {
                                            "field": "TotalPacketsCount"
                                            }
                                        },
                                        "SrcUplinkRole": {
                                            "terms": {
                                            "field": "SrcUplinkRole",
                                            "size": 5,
                                            "order": {
                                                "SumofBytes": "desc"
                                            }
                                            },
                                            "aggs": {
                                            "SumofBytes": {
                                                "sum": {
                                                "field": "TotalBytesCount"
                                                }
                                            },
                                            "SumofPackets": {
                                                "sum": {
                                                "field": "TotalPacketsCount"
                                                }
                                            },
                                            "DestinationNSG": {
                                                "terms": {
                                                "field": "DestinationNSG",
                                                "size": 5,
                                                "order": {
                                                    "SumofBytes": "desc"
                                                }
                                                },
                                                "aggs": {
                                                "SumofBytes": {
                                                    "sum": {
                                                    "field": "TotalBytesCount"
                                                    }
                                                },
                                                "SumofPackets": {
                                                    "sum": {
                                                    "field": "TotalPacketsCount"
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
                    }
                    }
                }
                }
            }
            }
         }
    )
    return response
