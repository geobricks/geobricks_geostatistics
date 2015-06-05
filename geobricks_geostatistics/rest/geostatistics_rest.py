import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from geobricks_common.core.log import logger

from geobricks_geostatistics.core.raster import Stats
from geobricks_geostatistics.config.config import config
from flask import request

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
        geostats = Stats(config)
        result = geostats.zonal_stats(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise Exception(e)


@app.route('/rasters/pixel/', methods=['POST'])
@app.route('/rasters/pixel', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_pixel_values_post():
    try:
        user_json = request.get_json()
        geostats = Stats(config)
        result = geostats.get_pixel_values_json(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise Exception(e)


@app.route('/rasters/stats/', methods=['POST'])
@app.route('/rasters/stats', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_stats_post():
    try:
        user_json = request.get_json()
        geostats = Stats(config)
        result = geostats.get_raster_stats_json(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise Exception(e)


@app.route('/rasters/histogram/', methods=['POST'])
@app.route('/rasters/histogram', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def get_histogram_post():
    try:
        user_json = request.get_json()
        geostats = Stats(config)
        result = geostats.get_raster_histogram_json(user_json)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise Exception(e)