from flask import Flask, render_template, jsonify
from vspk import v4_0 as vspk
from elasticsearch import Elasticsearch
import logging
import requests
from vspk.utils import set_log_level
from flask_cors import CORS, cross_origin
from app_from_nsg import stat as stat_app_from_nsg
from events import stat as stat_events
from sla_from_nsg import stat as stat_sla_from_nsg
from sla_to_nsg import stat as stat_sla_to_nsg
from top_10_apps import stat as stat_top_10_apps
from probestats_last_five_minutes import stat as probestasts_last_five_minutes
from probestats_top10 import stat as probestats_top_ten
from sentinella_port import stat as  utilization_apps
from sentinella_applications import stat as applicationsUse
from sentinella_violations import stat as violations
from branch_detail import detail
app = Flask(__name__)
CORS(app)
# Auth vars

vsd_ip = '192.168.0.20'
api_url = "https://192.168.0.20:8443"
username = "csproot"
password = "csproot"
enterprise = "csp"
"""
vsd_ip = '147.75.69.37'
api_url = "https://vsd1.sdn40r8.lab:8443" #"http://147.75.69.37:8443"
username = "csproot"
password = "csproot"
enterprise = "csp"
"""

clientE = Elasticsearch(['192.168.0.24:9200'])

def setup_logging():
    pass
    #set_log_level(logging.DEBUG, logging.Streamhandler())

def start_csproot_session():
    session = vspk.NUVSDSession(
        username=username,
        password=password,
        enterprise=enterprise,
        api_url=api_url
    )
    try:
        session.start()
    except:
        logging.error('Failed to start the session')
    return session.user


def vsc_health(csproot):
        data = {}
        for vsp in csproot.vsps.get():
            data['vscs'] = []
            data['name'] = vsp.name
            for vsc in vsp.vscs.get():
                data_vsc = vsc.to_dict()
                data_vsc['vrss'] = []
                for vrs in vsc.vrss.get():
                    vrs_dict = vrs.to_dict()
                    data_vsc['vrss'].append(vrs_dict)
                data['vscs'].append(data_vsc)
        return data

def nsg_health(csproot):
        data = {}
        for vsp in csproot.vsps.get():
            data['vscs'] = []
            data['name'] = vsp.name
            for vsc in vsp.vscs.get():
                data_vsc = vsc.to_dict()
                data_vsc['vrss'] = []
                for vrs in vsc.vrss.get():
                    vrs_dict = vrs.to_dict()
                    data_vsc['vrss'].append(vrs_dict)
                data['vscs'].append(data_vsc)
        return data

def applications(csproot):
    data = []
    enterprises = csproot.enterprises.get()
    for apps in enterprises[0].applications.get():
        data.append(apps.to_dict())
    return data

def detail(csproot):
    response = {}
    alarms = []
    for enterprise in csproot.enterprises.get(filter='ID is "6e51eafc-a2d7-4f6b-9a34-bb5262b60688"'):
        nsg_branch_up = 0
        nsg_branch_dow = 0
        nsgs = []
        
        vsc_up = 0
        vsc_down = 0
        
        for alarm in enterprise.alarms.get():
            alarms.append(alarm.to_dict())
        for g in enterprise.ns_redundant_gateway_groups.get(filter='ID is "79ad6616-3e75-4d98-b80f-efea2997d17a"'):
            for p in g.ns_gateways.get():
                if p.bootstrap_status != "ACTIVE":
                    nsg_branch_dow = nsg_branch_dow + 1
                else:
                    nsg_branch_up = nsg_branch_up +1
                nsg_ports = []
                for np in p.ns_ports.get():
                    nsg_port = {
                        "id": np.id,
                        "name": np.name,
                        "description" : np.description,
                        "status" : np.status,
                        "nsg-brach" : p.name,
                        "nsg-branch-id" : p.id
                    }
                    nsg_ports.append(nsg_port)


                nsg = {
                    "id": p.id,
                    "name": p.name,
                    "status" : p.bootstrap_status,
                    "cpu_usage" : 1.344,
                    "memory_usage" : 4.393,
                    "nsg_ports" : nsg_ports
                }
                nsgs.append(nsg)

                
        response['vsd_up'] = True
        elasticsearch_status = True
        if not clientE.ping():
            elasticsearch_status = False
        response['elasticsearch_up'] = elasticsearch_status
        response['vsc_up'] = 8
        response['vsc_down'] = 0
        response['nsg_up'] = 4
        response['nsg_down'] = 0
        response['nsgs'] = nsgs                   
        response['nsgs'] = nsgs
        response['nsg-branch-dow'] = nsg_branch_dow
        response['nsg-branch-up'] = nsg_branch_up

    response['alarms'] = alarms
    return response


@app.route('/')
#@cross_origin()
def table():
    setup_logging()
    csproot = start_csproot_session()
    return jsonify(vsc_health(csproot))
    #return render_template('table.html', vsp=vsc_health(csproot))

@app.route('/nsgs/')
#@cross_origin()
def nsg_detail():
    setup_logging()
    csproot = start_csproot_session()
    return jsonify(nsg_health(csproot))

@app.route('/applications')
#@cross_origin()
def apps():
    csproot = start_csproot_session()
    return jsonify(applications(csproot))

@app.route('/appfromnsg')
#@cross_origin()
def appfromnsg():
    return jsonify(stat_app_from_nsg()['hits'])

@app.route('/statevents')
#@cross_origin()
def statevents():
    return jsonify(stat_events()['hits'])

@app.route('/slafromnsg')
#@cross_origin()
def slafromnsg():
    return jsonify(stat_sla_from_nsg()['hits'])

@app.route('/slatonsg')
#@cross_origin()
def slatonsg():
    return jsonify(stat_sla_to_nsg()['hits'])

@app.route('/slastats')
#@cross_origin()
def slastats():
    URL = 'http://192.168.0.24:9200'
    DPI_sla_stats = requests.get(URL  + "/nuage_dpi_slastats-2017-05-10/_search?pretty")
    return jsonify(DPI_sla_stats.json())

@app.route('/top10apps')
#@cross_origin()
def top10apps():
    return jsonify(stat_top_10_apps()['hits'])

@app.route('/probestats-last-five-minutes/<string:SourceNSG>/<string:SrcUplink>/<string:interval>')
#@cross_origin()
def probestats(SourceNSG,SrcUplink,interval):
    return probestasts_last_five_minutes(SourceNSG,SrcUplink,interval)

@app.route('/utilization-ports/<string:SourceNSG>/<string:SrcUplink>/')
#@cross_origin()
def utilizationApps(SourceNSG,SrcUplink):
    return jsonify(utilization_apps(SourceNSG,SrcUplink))

@app.route('/utilization-applications/<string:SourceNSG>/<string:SrcUplink>/')
#@cross_origin()
def applicationsNSG(SourceNSG,SrcUplink):
    return jsonify(applicationsUse(SourceNSG,SrcUplink))

@app.route('/violations/<string:SourceNSG>/<string:SrcUplink>/')
#@cross_origin()
def violationsNSG(SourceNSG,SrcUplink):
    return jsonify(violations(SourceNSG,SrcUplink))

@app.route('/branch-details')
#@cross_origin()
def branch_detail_get():
    setup_logging()
    csproot = start_csproot_session()
    return jsonify(detail(csproot))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')

