import os
import json
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import get_raster_path
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery
from geobricks_gis_raster.core.raster import crop_raster_on_vector_bbox_and_postgis_db, get_statistics, get_srid, get_location_values

# crop_by_vector_database, get_statistics, get_srid, get_histogram, get_nodata_value, get_location_values

log = logger(__file__)


class Stats():

    # default settings
    config = None

    def __init__(self, config):
        self.config = config["settings"] if "settings" in config else config

    def zonal_stats(self, json_stats):
        '''
        :param json_stats: json with statistics definitions
        :return: json with response
        '''
        # Raster
        for raster in json_stats["raster"]:
            raster["path"] = get_raster_path(raster)
            # turning relative to absolute path if required
            if not os.path.isabs(raster["path"]):
                # this is used to normalize relative path used during test
                raster["path"] = os.path.normpath(os.path.join(os.path.dirname(__file__), raster["path"]))


        # Vector
        # TODO: make an ENUM somewhere (i.e. database, geojson, etc)
        if json_stats["vector"]["type"] == "database":
            return self._zonal_stats_by_vector_database(json_stats["raster"], json_stats["vector"]["options"], json_stats["stats"]["raster_stats"])
        elif json_stats["vector"]["type"] == "geojson":
            log.warn("TODO: Geojson statistics not implemented yet")

        # Stats
        # TODO: save stats in case is needed or return statistics
        return None

    def get_stats(self, json_stats):
        return get_statistics(get_raster_path(json_stats["raster"]))

    def get_histogram(self, json_stats):
        return get_statistics(get_raster_path(json_stats["raster"]), json_stats["stats"])

    def _zonal_stats_by_vector_database(self, rasters, vector, raster_statistics):

        # TODO remove dependency from here?
        sq = SpatialQuery(self.config)

        # Stats result
        all_stats = []

        # raster statistics
        # for each raster
        for raster in rasters:
            stats = []

            # get raster path
            raster_path = raster["path"]

            # Getting srid TODO: probably to apply in the crop process (GIS_raster method)
            srid = get_srid(raster_path)

            if raster_path is None:
                log.warn("Raster path is null for", raster)
            else:
                column_filter_code_index = 0
                column_filter_label_index = 1

                # get codes to use
                db_datasource = vector["db"]
                layer_code = vector["layer"]
                column_code = vector["column"]
                codes = vector["codes"]
                select = ",".join(vector["groupby"])
                groupyby = select
                query = sq.get_query_string_select_all(db_datasource, layer_code, column_code, codes, select, groupyby )
                subcodes = sq.query_db(vector["db"], query)

                # subcolumn_code
                subcolumn_code = vector["groupby"][column_filter_code_index]
                if subcodes:
                    for subcode in subcodes:
                        code = str(subcode[column_filter_code_index])
                        label = str(subcode[column_filter_label_index])
                        raster_stats = self._get_zonalstat_db(raster_path, srid, sq, db_datasource, layer_code, subcolumn_code, [code], raster_statistics)
                        obj = {"code": code, "label": label, "data": raster_stats}
                        stats.append(obj)

            # add to all stats
            all_stats.append(stats)
        return all_stats

    def _get_zonalstat_db(self, raster_path, srid, sq, db_datasource, layer_code, column_code, codes, raster_statistics):
        # retrieving bounding box
        bbox = sq.query_bbox(db_datasource, layer_code, column_code, codes, srid)

        # create the file on tm folder
        db = sq.get_db_instance()
        db_connection_string = db.get_connection_string(True)
        query = sq.get_query_string_select_all(db_datasource, layer_code, column_code, codes, "*")
        log.info(query)
        filepath = crop_raster_on_vector_bbox_and_postgis_db(raster_path, db_connection_string, query, bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
        return get_statistics(filepath, raster_statistics)

    def get_location_values(self, input_layers, lat, lon, band=None):
        input_files = []
        for input_layer in input_layers:
            input_files.append(self.get_raster_path(input_layer))
        log.info(input_files)
        return get_location_values(input_files, lat, lon, band)

#     def _zonal_stats_by_vector_database_old(self, json_stats):
#         # Stats result
#         all_stats = []
#
#         # raster statistics
#         raster_statistics = None if "raster_stats" not in json_stats["stats"] else json_stats["stats"]["raster_stats"]
#
#         # for each raster
#         for raster in json_stats["raster"]:
#             stats = []
#
#             # get raster path
#             raster_path = raster["path"]
#
#             # Getting srid TODO: probably to apply in the crop process (GIS_raster method)
#             srid = get_srid(raster_path)
#
#             if raster_path is None:
#                 log.warn("Raster path is null for", raster)
#             else:
#
#                 print raster_path
#
#                 # Query Options
#                 vector_opt = json_stats["vector"]["options"]
#
#                 # Change SCHEMA If exists
#                 opt = json.dumps(vector_opt)
#                 # TODO: how to handle it more clearly
#                 # TODO: the "." (dot) should be in the schema name?
#                 print self.db_spatial
#                 opt = opt.replace("{{SCHEMA}}", self.db_spatial.schema)
#                 vector_opt = json.loads(opt)
#
#                 # parsing results
#                 # the column filter is used to parse the
#                 column_filter = vector_opt['column_filter']
#
#                 # get column filter index
#                 # TODO: make it dynamic
#                 column_filter_code_index = 0
#                 column_filter_label_index = 1
#
#
#                 # retrieve query values
#                 select = vector_opt['query_condition']['select']
#                 from_query = vector_opt['query_condition']['from']
#                 where = None
#                 if "where" in vector_opt['query_condition']:
#                     where = vector_opt['query_condition']['where']
#                 # query DB
#                 codes = self.db_spatial.query_extented(select, from_query, where)
#
#                 if codes:
#                     for r in codes:
#                         code = str(r[column_filter_code_index])
#                         label = str(r[column_filter_label_index])
#                         # TODO: handle the ST_Transform somehow (i.e. transform the bounding box if srid is different?)
#                         #query_srid = "SELECT ST_SRID(geom) FROM gaul1_2015_4326 LIMIT 1;"
#                         query_extent = "SELECT ST_AsGeoJSON(ST_Extent(ST_Transform(geom, " + srid + "))) FROM " + from_query + " WHERE " + column_filter + " IN (" + code + ")"
#                         query_layer = "SELECT * FROM " + from_query + " WHERE " + column_filter + " IN (" + code + ")"
#                         filepath = crop_by_vector_database(raster_path, self.db_spatial, query_extent, query_layer)
#                         if filepath:
#                             raster_stats = get_statistics(filepath, raster_statistics)
#                             if raster_stats:
#                                 obj = {"code": code, "label": label, "data": raster_stats}
#                                 stats.append(obj)
#
#             # add to all stats
#             all_stats.append(stats)
#         return all_stats
#
#     def get_location_values(self, input_layers, lat, lon, band=None):
#         input_files = []
#         for input_layer in input_layers:
#             input_files.append(self.get_raster_path(input_layer))
#         log.info(input_files)
#         return get_location_values(input_files, lat, lon, band)
#
#
#
# # get the default db from the settings
# def get_default_db(settings, dtype, connect=True):
#     print "here"
#     try:
#         if "db" in settings:
#             print settings
#             db = settings["db"][dtype]
#             if connect:
#                 print "here"
#                 return DBMSPostgreSQL(db)
#             else:
#                 return db
#         return None
#     except:
#         log.warn("No db found")
#         pass