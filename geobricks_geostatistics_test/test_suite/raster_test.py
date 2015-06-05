import unittest
import simplejson
import requests
from geobricks_common.core.log import logger
from geobricks_geostatistics.core.raster import Stats
from geobricks_geostatistics.config.config import config

log = logger(__file__)

json_request = {
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
        },
        "pixel": {
            "lat": 35.16853,
            "lon": -6.0804
        }
    }
}



class GeobricksTest(unittest.TestCase):

    # def test_zonal_statistics(self):
    #     geostats = Stats(config)
    #     stats = geostats.zonal_stats(json_request)
    #     log.info(stats)
    #     self.assertEqual(stats, [[{'code': '1634', 'data': {'stats': [{'band': 1, 'max': 0.0021182389464229345, 'mean': 2.7871565084512296e-05, 'sd': 0.00024137483406419023, 'min': 0.0}]}, 'label': "Valle D'aosta"}, {'code': '1624', 'data': {'stats': [{'band': 1, 'max': 0.10968805104494095, 'mean': 0.03663491774051168, 'sd': 0.03906711456797175, 'min': 0.0}]}, 'label': 'Lombardia'}, {'code': '1632', 'data': {'stats': [{'band': 1, 'max': 0.009815381839871407, 'mean': 7.113129072013997e-05, 'sd': 0.0006209487653326749, 'min': 0.0}]}, 'label': 'Trentino-alto Adige'}, {'code': '1621', 'data': {'stats': [{'band': 1, 'max': 0.0033365213312208652, 'mean': 8.645712933753447e-05, 'sd': 0.0005098365067314013, 'min': 0.0}]}, 'label': 'Friuli-venezia Giulia'}, {'code': '1622', 'data': {'stats': [{'band': 1, 'max': 0.00020971079356968403, 'mean': 9.886644379135263e-07, 'sd': 1.3352858674824812e-05, 'min': 0.0}]}, 'label': 'Lazio'}, {'code': '1633', 'data': {'stats': [{'band': 1, 'max': 0.0005897823139093816, 'mean': 6.016727893047475e-06, 'sd': 5.2558115410160636e-05, 'min': 0.0}]}, 'label': 'Umbria'}, {'code': '1616', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Abruzzi'}, {'code': '1630', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Sicilia'}, {'code': '1635', 'data': {'stats': [{'band': 1, 'max': 0.08992145955562592, 'mean': 0.002678981771393438, 'sd': 0.005260116188983823, 'min': 0.0}]}, 'label': 'Veneto'}, {'code': '1625', 'data': {'stats': [{'band': 1, 'max': 0.003014434827491641, 'mean': 2.7426076233030506e-05, 'sd': 0.00027637394918476627, 'min': 0.0}]}, 'label': 'Marche'}, {'code': '1627', 'data': {'stats': [{'band': 1, 'max': 0.1521584540605545, 'mean': 0.04313715813342962, 'sd': 0.051576567862514786, 'min': 0.0}]}, 'label': 'Piemonte'}, {'code': '1629', 'data': {'stats': [{'band': 1, 'max': 0.010474860668182373, 'mean': 0.0014162321573680447, 'sd': 0.0021409244796609136, 'min': 0.0}]}, 'label': 'Sardegna'}, {'code': '1618', 'data': {'stats': [{'band': 1, 'max': 0.0009458046406507492, 'mean': 0.00028004215186808943, 'sd': 0.00028287835544453554, 'min': 0.0}]}, 'label': 'Calabria'}, {'code': '1620', 'data': {'stats': [{'band': 1, 'max': 0.10085176676511765, 'mean': 0.005518219278016517, 'sd': 0.012279702406774468, 'min': 0.0}]}, 'label': 'Emilia-romagna'}, {'code': '1623', 'data': {'stats': [{'band': 1, 'max': 0.010794335976243019, 'mean': 0.00011569839026918016, 'sd': 0.0010311318639328992, 'min': 0.0}]}, 'label': 'Liguria'}, {'code': '1628', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Puglia'}, {'code': '1619', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Campania'}, {'code': '1617', 'data': {'stats': [{'band': 1, 'max': 0.00016816887364257127, 'mean': 1.3422543829688381e-06, 'sd': 1.3201455434292494e-05, 'min': 0.0}]}, 'label': 'Basilicata'}, {'code': '1631', 'data': {'stats': [{'band': 1, 'max': 0.0011568577028810978, 'mean': 0.00016217358395328798, 'sd': 0.00016893858107417596, 'min': 0.0}]}, 'label': 'Toscana'}, {'code': '1626', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Molise'}], [{'code': '1634', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': "Valle D'aosta"}, {'code': '1624', 'data': {'stats': [{'band': 1, 'max': 0.10968805104494095, 'mean': 0.03763265257946655, 'sd': 0.039455910668251194, 'min': 0.0}]}, 'label': 'Lombardia'}, {'code': '1632', 'data': {'stats': [{'band': 1, 'max': 0.009815381839871407, 'mean': 7.125913057736564e-05, 'sd': 0.0006919502489041021, 'min': 0.0}]}, 'label': 'Trentino-alto Adige'}, {'code': '1621', 'data': {'stats': [{'band': 1, 'max': 0.0031851886305958033, 'mean': 2.785258604070315e-05, 'sd': 0.0002805813436557818, 'min': 0.0}]}, 'label': 'Friuli-venezia Giulia'}, {'code': '1622', 'data': {'stats': [{'band': 1, 'max': 0.0003079786547459662, 'mean': 1.6714522221791889e-06, 'sd': 2.059340261562904e-05, 'min': 0.0}]}, 'label': 'Lazio'}, {'code': '1633', 'data': {'stats': [{'band': 1, 'max': 0.00039232365088537335, 'mean': 3.0650285225419793e-06, 'sd': 3.454111724000073e-05, 'min': 0.0}]}, 'label': 'Umbria'}, {'code': '1616', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Abruzzi'}, {'code': '1630', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Sicilia'}, {'code': '1635', 'data': {'stats': [{'band': 1, 'max': 0.0033365213312208652, 'mean': 0.002370884219326648, 'sd': 0.001182530562854639, 'min': 0.0}]}, 'label': 'Veneto'}, {'code': '1625', 'data': {'stats': [{'band': 1, 'max': 0.003014434827491641, 'mean': 3.6556521550782265e-05, 'sd': 0.00032040155999435123, 'min': 0.0}]}, 'label': 'Marche'}, {'code': '1627', 'data': {'stats': [{'band': 1, 'max': 0.1521584540605545, 'mean': 0.04337544519433324, 'sd': 0.05157260088388939, 'min': 0.0}]}, 'label': 'Piemonte'}, {'code': '1629', 'data': {'stats': [{'band': 1, 'max': 0.010474860668182373, 'mean': 0.0014096522556449119, 'sd': 0.0021320714602314217, 'min': 0.0}]}, 'label': 'Sardegna'}, {'code': '1618', 'data': {'stats': [{'band': 1, 'max': 0.0009458046406507492, 'mean': 0.000288605523520048, 'sd': 0.0002870308749937403, 'min': 0.0}]}, 'label': 'Calabria'}, {'code': '1620', 'data': {'stats': [{'band': 1, 'max': 0.10085176676511765, 'mean': 0.005163787119562184, 'sd': 0.010731503925804173, 'min': 0.0}]}, 'label': 'Emilia-romagna'}, {'code': '1623', 'data': {'stats': [{'band': 1, 'max': 0.010794335976243019, 'mean': 0.00015958548995446864, 'sd': 0.0012075477070897119, 'min': 0.0}]}, 'label': 'Liguria'}, {'code': '1628', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Puglia'}, {'code': '1619', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Campania'}, {'code': '1617', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Basilicata'}, {'code': '1631', 'data': {'stats': [{'band': 1, 'max': 0.0006882257875986397, 'mean': 0.0001563581044873189, 'sd': 0.0001624167825228153, 'min': 0.0}]}, 'label': 'Toscana'}, {'code': '1626', 'data': {'stats': [{'band': 1, 'max': 0.0, 'mean': 0.0, 'sd': 0.0, 'min': 0.0}]}, 'label': 'Molise'}]])
    #
    # def test_zonal_statistics_rest(self):
    #     headers = {'content-type': 'application/json'}
    #     data = simplejson.dumps(json_request)
    #     r = requests.post("http://localhost:5915/geostatistics/rasters/zonalstats/", data=data, headers=headers)
    #     result = simplejson.loads(r.text)
    #     self.assertEqual(result, [[{"code": "1634", "data": {"stats": [{"band": 1, "max": 0.0021182389464229345, "mean": 2.7871565084512296e-05, "sd": 0.00024137483406419023, "min": 0.0}]}, "label": "Valle D'aosta"}, {"code": "1624", "data": {"stats": [{"band": 1, "max": 0.10968805104494095, "mean": 0.03663491774051168, "sd": 0.03906711456797175, "min": 0.0}]}, "label": "Lombardia"}, {"code": "1632", "data": {"stats": [{"band": 1, "max": 0.009815381839871407, "mean": 7.113129072013997e-05, "sd": 0.0006209487653326749, "min": 0.0}]}, "label": "Trentino-alto Adige"}, {"code": "1621", "data": {"stats": [{"band": 1, "max": 0.0033365213312208652, "mean": 8.645712933753447e-05, "sd": 0.0005098365067314013, "min": 0.0}]}, "label": "Friuli-venezia Giulia"}, {"code": "1622", "data": {"stats": [{"band": 1, "max": 0.00020971079356968403, "mean": 9.886644379135263e-07, "sd": 1.3352858674824812e-05, "min": 0.0}]}, "label": "Lazio"}, {"code": "1633", "data": {"stats": [{"band": 1, "max": 0.0005897823139093816, "mean": 6.016727893047475e-06, "sd": 5.2558115410160636e-05, "min": 0.0}]}, "label": "Umbria"}, {"code": "1616", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Abruzzi"}, {"code": "1630", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Sicilia"}, {"code": "1635", "data": {"stats": [{"band": 1, "max": 0.08992145955562592, "mean": 0.002678981771393438, "sd": 0.005260116188983823, "min": 0.0}]}, "label": "Veneto"}, {"code": "1625", "data": {"stats": [{"band": 1, "max": 0.003014434827491641, "mean": 2.7426076233030506e-05, "sd": 0.00027637394918476627, "min": 0.0}]}, "label": "Marche"}, {"code": "1627", "data": {"stats": [{"band": 1, "max": 0.1521584540605545, "mean": 0.04313715813342962, "sd": 0.051576567862514786, "min": 0.0}]}, "label": "Piemonte"}, {"code": "1629", "data": {"stats": [{"band": 1, "max": 0.010474860668182373, "mean": 0.0014162321573680447, "sd": 0.0021409244796609136, "min": 0.0}]}, "label": "Sardegna"}, {"code": "1618", "data": {"stats": [{"band": 1, "max": 0.0009458046406507492, "mean": 0.00028004215186808943, "sd": 0.00028287835544453554, "min": 0.0}]}, "label": "Calabria"}, {"code": "1620", "data": {"stats": [{"band": 1, "max": 0.10085176676511765, "mean": 0.005518219278016517, "sd": 0.012279702406774468, "min": 0.0}]}, "label": "Emilia-romagna"}, {"code": "1623", "data": {"stats": [{"band": 1, "max": 0.010794335976243019, "mean": 0.00011569839026918016, "sd": 0.0010311318639328992, "min": 0.0}]}, "label": "Liguria"}, {"code": "1628", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Puglia"}, {"code": "1619", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Campania"}, {"code": "1617", "data": {"stats": [{"band": 1, "max": 0.00016816887364257127, "mean": 1.3422543829688381e-06, "sd": 1.3201455434292494e-05, "min": 0.0}]}, "label": "Basilicata"}, {"code": "1631", "data": {"stats": [{"band": 1, "max": 0.0011568577028810978, "mean": 0.00016217358395328798, "sd": 0.00016893858107417596, "min": 0.0}]}, "label": "Toscana"}, {"code": "1626", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Molise"}], [{"code": "1634", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Valle D'aosta"}, {"code": "1624", "data": {"stats": [{"band": 1, "max": 0.10968805104494095, "mean": 0.03763265257946655, "sd": 0.039455910668251194, "min": 0.0}]}, "label": "Lombardia"}, {"code": "1632", "data": {"stats": [{"band": 1, "max": 0.009815381839871407, "mean": 7.125913057736564e-05, "sd": 0.0006919502489041021, "min": 0.0}]}, "label": "Trentino-alto Adige"}, {"code": "1621", "data": {"stats": [{"band": 1, "max": 0.0031851886305958033, "mean": 2.785258604070315e-05, "sd": 0.0002805813436557818, "min": 0.0}]}, "label": "Friuli-venezia Giulia"}, {"code": "1622", "data": {"stats": [{"band": 1, "max": 0.0003079786547459662, "mean": 1.6714522221791889e-06, "sd": 2.059340261562904e-05, "min": 0.0}]}, "label": "Lazio"}, {"code": "1633", "data": {"stats": [{"band": 1, "max": 0.00039232365088537335, "mean": 3.0650285225419793e-06, "sd": 3.454111724000073e-05, "min": 0.0}]}, "label": "Umbria"}, {"code": "1616", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Abruzzi"}, {"code": "1630", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Sicilia"}, {"code": "1635", "data": {"stats": [{"band": 1, "max": 0.0033365213312208652, "mean": 0.002370884219326648, "sd": 0.001182530562854639, "min": 0.0}]}, "label": "Veneto"}, {"code": "1625", "data": {"stats": [{"band": 1, "max": 0.003014434827491641, "mean": 3.6556521550782265e-05, "sd": 0.00032040155999435123, "min": 0.0}]}, "label": "Marche"}, {"code": "1627", "data": {"stats": [{"band": 1, "max": 0.1521584540605545, "mean": 0.04337544519433324, "sd": 0.05157260088388939, "min": 0.0}]}, "label": "Piemonte"}, {"code": "1629", "data": {"stats": [{"band": 1, "max": 0.010474860668182373, "mean": 0.0014096522556449119, "sd": 0.0021320714602314217, "min": 0.0}]}, "label": "Sardegna"}, {"code": "1618", "data": {"stats": [{"band": 1, "max": 0.0009458046406507492, "mean": 0.000288605523520048, "sd": 0.0002870308749937403, "min": 0.0}]}, "label": "Calabria"}, {"code": "1620", "data": {"stats": [{"band": 1, "max": 0.10085176676511765, "mean": 0.005163787119562184, "sd": 0.010731503925804173, "min": 0.0}]}, "label": "Emilia-romagna"}, {"code": "1623", "data": {"stats": [{"band": 1, "max": 0.010794335976243019, "mean": 0.00015958548995446864, "sd": 0.0012075477070897119, "min": 0.0}]}, "label": "Liguria"}, {"code": "1628", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Puglia"}, {"code": "1619", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Campania"}, {"code": "1617", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Basilicata"}, {"code": "1631", "data": {"stats": [{"band": 1, "max": 0.0006882257875986397, "mean": 0.0001563581044873189, "sd": 0.0001624167825228153, "min": 0.0}]}, "label": "Toscana"}, {"code": "1626", "data": {"stats": [{"band": 1, "max": 0.0, "mean": 0.0, "sd": 0.0, "min": 0.0}]}, "label": "Molise"}]])

    def test_pixel_values(self):
        geostats = Stats(config)
        stats = geostats.get_pixel_values_json(json_request)
        self.assertEqual(stats, [0.00137174816336483, 0.000445023528300226])

    def test_pixel_values_rest(self):
        headers = {'content-type': 'application/json'}
        data = simplejson.dumps(json_request)
        r = requests.post("http://localhost:5915/geostatistics/rasters/pixel/", data=data, headers=headers)
        result = simplejson.loads(r.text)
        self.assertEqual(result, [0.00137174816336483, 0.000445023528300226])


    def test_stats(self):
        geostats = Stats(config)
        stats = geostats.get_raster_stats_json(json_request)
        print stats
        self.assertEqual(stats, {'stats': [{'band': 1, 'max': 1.8875657320022583, 'mean': 0.005638870409654933, 'sd': 0.045585188037842256, 'min': 0.0}]}                         )

    def test_histogram(self):
        geostats = Stats(config)
        stats = geostats.get_raster_histogram_json(json_request)
        print stats
        self.assertEqual(stats, {'hist': [{'band': 1, 'buckets': 256, 'values': [2117478, 24871, 13849, 8977, 6419, 4961, 4136, 3441, 2939, 2693, 2425, 2254, 1992, 2252, 1543, 1371, 1212, 1159, 1147, 1063, 1007, 951, 841, 750, 734, 717, 720, 620, 628, 608, 563, 472, 510, 463, 546, 464, 464, 437, 435, 374, 399, 337, 356, 401, 319, 314, 272, 296, 316, 260, 258, 278, 230, 224, 209, 236, 241, 218, 165, 196, 145, 161, 163, 121, 137, 137, 122, 122, 142, 147, 133, 130, 120, 122, 145, 135, 98, 85, 85, 91, 102, 69, 76, 65, 65, 76, 78, 66, 60, 69, 57, 53, 54, 51, 56, 53, 46, 71, 56, 44, 47, 49, 49, 39, 65, 42, 38, 52, 52, 41, 36, 69, 48, 39, 43, 23, 41, 33, 43, 40, 42, 53, 34, 54, 39, 39, 35, 53, 28, 39, 20, 27, 30, 27, 26, 22, 30, 26, 32, 22, 23, 38, 25, 14, 14, 12, 14, 20, 9, 8, 14, 3, 8, 18, 16, 29, 10, 4, 2, 6, 11, 3, 19, 7, 3, 5, 5, 1, 5, 2, 5, 6, 3, 0, 5, 5, 3, 5, 13, 7, 2, 2, 3, 2, 6, 5, 4, 2, 4, 3, 6, 3, 3, 2, 17, 1, 4, 1, 3, 12, 1, 1, 0, 1, 1, 1, 1, 2, 0, 1, 1, 2, 0, 0, 3, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 'max': 1.8875657320022583, 'min': 0.0}], 'stats': [{'band': 1, 'max': 1.8875657320023, 'mean': 0.0056388704096549, 'sd': 0.045585188037842, 'min': 0.0}]})


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()


