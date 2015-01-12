import json
import os
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from geobricks_common.core.log import logger

from geobricks_geostatistics.core.raster import Stats
from geobricks_geostatistics.config.config import config
from flask import request, send_from_directory

log = logger(__file__)

app = Blueprint("geostatistics", "geostatistics")


@app.route('/')
@cross_origin(origins='*')
def root():
    """
    Root REST service.
    @return: Welcome message.
    """
    return 'Welcome to Geobricks Geostatistics!'


@app.route('/discovery/')
@app.route('/discovery')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'Geostatistics service',
        'description': 'Functionalities to compute geostatistics.',
        'type': 'SERVICE'
    }
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/rasters/zonalstats/', methods=['POST'])
@app.route('/rasters/zonalstats', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_rasters_spatial_query():
    try:
        user_json = request.get_json()
        #TODO: handle it nicer the url to set the distribution download url
        geostats = Stats(config)
        result = geostats.zonal_stats(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise Exception(e)
