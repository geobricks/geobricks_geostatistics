import unittest
from geobricks_common.core.log import logger
from geobricks_geostatistics.core.raster import Stats
from geobricks_geostatistics.config.config import config

log = logger(__file__)

# json_stats = {
#     "raster": [
#         {
#                # "uid": "fenix:rice_area1",
#                 "workspace": "workspace",
#                 "layerName": "rice_area_3857",
#                 "datasource": "geoserver",
#                 "_name": "optional",
#                 "_path": "optional"
#         },
#         {
#             # "uid": "fenix:rice_area1",
#             "workspace": "workspace",
#             "layerName": "rice_area_4326",
#             "datasource": "storage",
#             "_name": "optional",
#             "_path": "optional"
#         }
#     ],
#     "vector":
#         {
#             # It's the name of the gaul spatial table
#             "name": "gaul1",
#
#             # Database
#             "type": "database",
#             "options": {
#
#                 # used to query the db and retrieve the right codes
#                 "query_condition" : {
#                     "select": "adm1_code, adm1_name",
#                     "from": "{{SCHEMA}}.gaul1_2015_4326",
#                     "where": "adm0_name IN ('Italy') GROUP BY adm1_code, adm1_name ",
#                 },
#
#                 # used to subquery the db to get the geometry and process the raster
#                 "column_filter": "adm1_code",
#
#                 # used to fill stats table (raster["name"].vector["name"])
#                 #"stats_columns" : {
#                 #    "polygon_id": "adm1_code",
#                 #    "label_en": "adm1_name",
#                 #}
#             },
#
#             # TODO: GeoJson (Problem how to save the geojson fields? Just gives back the result without saving them)
#             # "type" : "geojson",
#             # "path" : "/hove/Desktop/GIS/layer.geojson",
#         }
#     ,
#     "stats" : {
#         #"force": True,
#
#         # default is false (return just the json with the statistics)
#         #"save_stats": True,
#
#         #  default option
#         "delete_tmp_files": True,
#
#         # STATISTICS
#         "raster_stats": {
#             "descriptive_stats": {
#                 "force": True
#             },
#             # "histogram": {
#             #     "buckets": 256,
#             #     "include_out_of_range": 0,
#             #     "force": True
#             # }
#         }
#     }
# }



json_stats = {
    "raster": [
        {
            # "uid": "fenix:rice_area1",
            "workspace": "workspace",
            "layerName": "rice_area_3857",
            "datasource": "geoserver",
            "_name": "optional",
            "_path": "optional"
        },
        {
            # "uid": "fenix:rice_area1",
            "workspace": "workspace",
            "layerName": "rice_area_4326",
            "datasource": "storage",
            "_name": "optional",
            "_path": "optional"
        }
    ],
    "vector":
        {
            # # It's the name of the gaul spatial table
            # "name": "gaul1",

            # Database
            "type": "database",
            "options": {
                "db": "spatial",    #optional
                "layer": "gaul1_2015_4326",  # required (table or table alias)
                "column": "adm0_name",  # required (column or column_alias)
                "codes": ["Italy"],
                "groupby": ["adm1_code", "adm1_name"]  # optional used to get subcodes (i.e. get all italian's region)
            }
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
        }
    }
}



class GeobricksTest(unittest.TestCase):

    def test_distribution_geoserver(self):
        geostats = Stats(config)
        stats = geostats.zonal_stats(json_stats)
        log.info(stats)
        self.assertEqual(stats, [[{'code': '1634', 'data': {'stats': [{'band': 1, 'max': 0.009865675121545792, 'mean': 0.00018937244116292373, 'sd': 0.0012316753478514328, 'min': 0.0}]}, 'label': "Valle D'aosta"}, {'code': '1624', 'data': {'stats': [{'band': 1, 'max': 0.14426584541797638, 'mean': 0.018474885500022912, 'sd': 0.03355921764272358, 'min': 0.0}]}, 'label': 'Lombardia'}, {'code': '1632', 'data': {'stats': [{'band': 1, 'max': 0.00227531255222857, 'mean': 7.0395780768544724e-06, 'sd': 0.00012036302877133285, 'min': 0.0}]}, 'label': 'Trentino-alto Adige'}, {'code': '1621', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Friuli-venezia Giulia'}, {'code': '1622', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Lazio'}, {'code': '1633', 'data': {'stats': [{'band': 1, 'max': 0.0005897823139093816, 'mean': 3.4941718135646975e-06, 'sd': 4.183726155912045e-05, 'min': 0.0}]}, 'label': 'Umbria'}, {'code': '1616', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Abruzzi'}, {'code': '1630', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Sicilia'}, {'code': '1635', 'data': {'stats': [{'band': 1, 'max': 0.0033365213312208652, 'mean': 0.0009797784690643945, 'sd': 0.0013878881389672772, 'min': 0.0}]}, 'label': 'Veneto'}, {'code': '1625', 'data': {'stats': [{'band': 1, 'max': 0.004310854244977236, 'mean': 2.5598089183297226e-05, 'sd': 0.00030581024377528034, 'min': 0.0}]}, 'label': 'Marche'}, {'code': '1627', 'data': {'stats': [{'band': 1, 'max': 0.1521584540605545, 'mean': 0.02113632266756819, 'sd': 0.042558039876362745, 'min': 0.0}]}, 'label': 'Piemonte'}, {'code': '1629', 'data': {'stats': [{'band': 1, 'max': 0.010474860668182373, 'mean': 0.0008340506626457985, 'sd': 0.0017558976877441101, 'min': 0.0}]}, 'label': 'Sardegna'}, {'code': '1618', 'data': {'stats': [{'band': 1, 'max': 0.0009458046406507492, 'mean': 0.00012039904126769541, 'sd': 0.00023709935045922864, 'min': 0.0}]}, 'label': 'Calabria'}, {'code': '1620', 'data': {'stats': [{'band': 1, 'max': 0.08743440359830856, 'mean': 0.0024925661351449823, 'sd': 0.0073751312756450875, 'min': 0.0}]}, 'label': 'Emilia-romagna'}, {'code': '1623', 'data': {'stats': [{'band': 1, 'max': 0.010794335976243019, 'mean': 5.9750989136217766e-05, 'sd': 0.0007367232666277575, 'min': 0.0}]}, 'label': 'Liguria'}, {'code': '1628', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Puglia'}, {'code': '1619', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Campania'}, {'code': '1617', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Basilicata'}, {'code': '1631', 'data': {'stats': [{'band': 1, 'max': 0.0011568577028810978, 'mean': 7.563164246058867e-05, 'sd': 0.00015014820908528946, 'min': 0.0}]}, 'label': 'Toscana'}, {'code': '1626', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Molise'}], [{'code': '1634', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': "Valle D'aosta"}, {'code': '1624', 'data': {'stats': [{'band': 1, 'max': 0.10968805104494095, 'mean': 0.03763265257946655, 'sd': 0.039455910668251194, 'min': 0.0}]}, 'label': 'Lombardia'}, {'code': '1632', 'data': {'stats': [{'band': 1, 'max': 0.009815381839871407, 'mean': 7.125913057736564e-05, 'sd': 0.0006919502489041021, 'min': 0.0}]}, 'label': 'Trentino-alto Adige'}, {'code': '1621', 'data': {'stats': [{'band': 1, 'max': 0.0031851886305958033, 'mean': 2.785258604070315e-05, 'sd': 0.0002805813436557818, 'min': 0.0}]}, 'label': 'Friuli-venezia Giulia'}, {'code': '1622', 'data': {'stats': [{'band': 1, 'max': 0.0003079786547459662, 'mean': 1.6714522221791889e-06, 'sd': 2.059340261562904e-05, 'min': 0.0}]}, 'label': 'Lazio'}, {'code': '1633', 'data': {'stats': [{'band': 1, 'max': 0.00039232365088537335, 'mean': 3.0650285225419793e-06, 'sd': 3.454111724000073e-05, 'min': 0.0}]}, 'label': 'Umbria'}, {'code': '1616', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Abruzzi'}, {'code': '1630', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Sicilia'}, {'code': '1635', 'data': {'stats': [{'band': 1, 'max': 0.0033365213312208652, 'mean': 0.002370884219326648, 'sd': 0.001182530562854639, 'min': 0.0}]}, 'label': 'Veneto'}, {'code': '1625', 'data': {'stats': [{'band': 1, 'max': 0.003014434827491641, 'mean': 3.6556521550782265e-05, 'sd': 0.00032040155999435123, 'min': 0.0}]}, 'label': 'Marche'}, {'code': '1627', 'data': {'stats': [{'band': 1, 'max': 0.1521584540605545, 'mean': 0.04337544519433324, 'sd': 0.05157260088388939, 'min': 0.0}]}, 'label': 'Piemonte'}, {'code': '1629', 'data': {'stats': [{'band': 1, 'max': 0.010474860668182373, 'mean': 0.0014096522556449119, 'sd': 0.0021320714602314217, 'min': 0.0}]}, 'label': 'Sardegna'}, {'code': '1618', 'data': {'stats': [{'band': 1, 'max': 0.0009458046406507492, 'mean': 0.000288605523520048, 'sd': 0.0002870308749937403, 'min': 0.0}]}, 'label': 'Calabria'}, {'code': '1620', 'data': {'stats': [{'band': 1, 'max': 0.10085176676511765, 'mean': 0.005163787119562184, 'sd': 0.010731503925804173, 'min': 0.0}]}, 'label': 'Emilia-romagna'}, {'code': '1623', 'data': {'stats': [{'band': 1, 'max': 0.010794335976243019, 'mean': 0.00015958548995446864, 'sd': 0.0012075477070897119, 'min': 0.0}]}, 'label': 'Liguria'}, {'code': '1628', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Puglia'}, {'code': '1619', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Campania'}, {'code': '1617', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Basilicata'}, {'code': '1631', 'data': {'stats': [{'band': 1, 'max': 0.0006882257875986397, 'mean': 0.0001563581044873189, 'sd': 0.0001624167825228153, 'min': 0.0}]}, 'label': 'Toscana'}, {'code': '1626', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Molise'}]])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


