from elasticsearch import Elasticsearch

client = Elasticsearch(['192.168.0.24:9200'])

def stat():
    response = client.search(
        index="nuage_event",
        body={
        "aggs": {
            "2": {
                "filters":{
                "filters":{
                    "Domain":{
                    "query":{
                        "term":{
                        "nuage_metadata.enterpriseName":"chord_enterprise"
                        }
                    }
                    }
                }
                },
                "aggs": {
                "timezones": {
                    "filters": {
                    "filters": {
                        "Prev 24": {
                        "range": {
                            "timestamp": {
                            "gte": "now-48h",
                            "lte": "now-24h"
                            }
                        }
                        },
                        "Last 24": {
                        "range": {
                            "timestamp": {
                            "gte": "now-24h",
                            "lte": "now"
                            }
                        }
                        }
                    }
                    },
                    "aggs": {
                    "types": {
                        "filters": {
                        "filters": {
                            "type": {
                            "query": {
                                "term": {
                                "type": "TCA_EVENT"
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
