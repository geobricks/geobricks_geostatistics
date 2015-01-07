import unittest
from geobricks_geostatistics.core.raster import Stats
from geobricks_geostatistics.config.config import config

json_stats = {
    "raster": [
        {
               # "uid": "fenix:rice_area1",
                "workspace": "fenix",
                "layerName": "rice_area1",
                "datasource":"geoserver",
                "_name": "optional",
                "_path": "optional"
        }
    ],
    "vector":
        {
            # It's the name of the gaul spatial table
            "name": "gaul1",

            # Database
            "type": "database",
            "options": {

                # used to query the db and retrieve the right codes
                "query_condition" : {
                    "select": "adm1_code, adm1_name",
                    "from": "{{SCHEMA}}.gaul1_2015_4326",
                    "where": "adm0_name IN ('Italy') GROUP BY adm1_code, adm1_name ",
                },

                # used to subquery the db to get the geometry and process the raster
                "column_filter": "adm1_code",

                # used to fill stats table (raster["name"].vector["name"])
                #"stats_columns" : {
                #    "polygon_id": "adm1_code",
                #    "label_en": "adm1_name",
                #}
            },

            # TODO: GeoJson (Problem how to save the geojson fields? Just gives back the result without saving them)
            # "type" : "geojson",
            # "path" : "/hove/Desktop/GIS/layer.geojson",
        }
    ,
    "stats" : {
        #"force": True,

        # default is false (return just the json with the statistics)
        #"save_stats": True,

        #  default option
        "delete_tmp_files": True,

        # STATISTICS
        "raster_stats": {
            "descriptive_stats": {
                "force": True
            },
            # "histogram": {
            #     "buckets": 256,
            #     "include_out_of_range": 0,
            #     "force": True
            # }
        }
    }
}






class GeobricksTest(unittest.TestCase):

    def test_example(self):
        geostats = Stats(config)
        stats1 = geostats.zonal_stats(json_stats)
        print stats1


