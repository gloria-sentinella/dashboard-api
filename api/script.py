from flask import Flask, render_template, jsonify
from vspk import v4_0 as vspk
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
app = Flask(__name__)

# Auth vars
vsd_ip = '192.168.0.20'
api_url = "https://192.168.0.20:8443"
username = "csproot"
password = "csproot"
enterprise = "csp"

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

def applications(csproot):
    data = []
    enterprises = csproot.enterprises.get()
    for apps in enterprises[0].applications.get():
        data.append(apps.to_dict())
    return data

@app.route('/')
@cross_origin()
def table():
    setup_logging()
    csproot = start_csproot_session()
    return jsonify(vsc_health(csproot))
    #return render_template('table.html', vsp=vsc_health(csproot))

@app.route('/applications')
@cross_origin()
def apps():
    csproot = start_csproot_session()
    return jsonify(applications(csproot))

@app.route('/appfromnsg')
@cross_origin()
def appfromnsg():
    return jsonify(stat_app_from_nsg()['hits'])

@app.route('/statevents')
@cross_origin()
def statevents():
    return jsonify(stat_events()['hits'])

@app.route('/slafromnsg')
@cross_origin()
def slafromnsg():
    return jsonify(stat_sla_from_nsg()['hits'])

@app.route('/slatonsg')
@cross_origin()
def slatonsg():
    return jsonify(stat_sla_to_nsg()['hits'])

@app.route('/slastats')
@cross_origin()
def slastats():
    URL = 'http://192.168.0.24:9200'
    DPI_sla_stats = requests.get(URL  + "/nuage_dpi_slastats-2017-05-10/_search?pretty")
    return jsonify(DPI_sla_stats.json())

@app.route('/top10apps')
@cross_origin()
def top10apps():
    return jsonify(stat_top_10_apps()['hits'])

@app.route('/probestats-last-five-minutes/<string:SourceNSG>/<string:SrcUplink>/<string>:interval>')
@cross_origin()
def probestats():
    return jsonify(probestasts_last_five_minutes(SourceNSG,SrcUplin,intervalk))

@app.route('/probestats-top-ten/<string:SourceNSG>/<string:SrcUplink>/')
@cross_origin()
def probestatsTopTen():
    return jsonify(probestasts_top_ten(SourceNSG,SrcUplink))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')

