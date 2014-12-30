import os
import json
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import get_raster_path_by_uid, get_raster_path_by_ftp_uid
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
from geobricks_gis_raster.core.raster import crop_by_vector_database, get_statistics, get_histogram, get_nodata_value, get_location_values

log = logger(__file__)


class Stats():

    # default settings
    settings = None
    #db_stats = None
    db_spatial = None

    def __init__(self, config):

        self.settings = config["settings"]

        # db_stats will connect to the database
        #self.db_stats = _get_default_db("stats", True)

        # db_stats will NOT connect to the database
        self.db_spatial = get_default_db(self.settings, "spatial", True)

    def zonal_stats(self, json_stats):
        stats = None
        # TODO: a common zonalstats
        '''
        :param json_stats: json with statistics definitions
        :return: json with response
        '''

        # Raster
        # if the raster is a raster store in the datadir
        if "uid" in json_stats["raster"]:
            json_stats["raster"]["path"] = get_raster_path_by_uid(json_stats["raster"]["uid"])

        # Vector
        # TODO: make an ENUM somewhere (i.e. database, geojson, etc)
        #log.info(json_stats["vector"]["type"])
        if json_stats["vector"]["type"] == "database":
            stats = self._zonal_stats_by_vector_database(json_stats)
        elif json_stats["vector"]["type"] == "geojson":
            log.warn("TODO: Geojson statistics")

        # Stats
        # TODO: save stats in case is needed or return statistics
        return stats

    def get_stats(self, json_stats):
        if "uid" in json_stats["raster"]:
            json_stats["raster"]["path"] = get_raster_path_by_uid(json_stats["raster"]["uid"])
        return get_statistics(json_stats["raster"]["path"])

    def get_histogram(self, json_stats):
        if "uid" in json_stats["raster"] and json_stats["raster"]["uid"] is not None:
            json_stats["raster"]["path"] = get_raster_path_by_uid(json_stats["raster"]["uid"])
        return get_histogram(json_stats["raster"]["path"], json_stats["stats"])


    def _zonal_stats_by_vector_database(self, json_stats):
        # Stats result
        stats = []

        # raster statistics
        raster_statistics = None if "raster_stats" not in json_stats["stats"] else json_stats["stats"]["raster_stats"]

        # Raster path
        #log.info(json_stats["raster"])
        raster_path = json_stats["raster"]["path"]

        # Query Options
        vector_opt = json_stats["vector"]["options"]

        # Change SCHEMA If exists
        opt = json.dumps(vector_opt)
        # TODO: how to handle it more clearly
        # TODO: the "." (dot) should be in the schema name?
        print self.db_spatial
        opt = opt.replace("{{SCHEMA}}", self.db_spatial.schema)
        vector_opt = json.loads(opt)

        # retrieve query values
        select = vector_opt['query_condition']['select']
        from_query = vector_opt['query_condition']['from']
        where = None
        if "where" in vector_opt['query_condition']:
            where = vector_opt['query_condition']['where']

        # build query
        query = "SELECT " + select + " FROM "+ from_query
        if ( where is not None):
            query += " WHERE " + where

        #log.info(query)

        # parsing results
        # the column filter is used to parse the
        column_filter = vector_opt['column_filter']

        # get column filter index
        # TODO: make it dynamic
        column_filter_code_index = 0
        column_filter_label_index = 1

        srcnodatavalue = get_nodata_value(raster_path)
        # log.info("SRC NODATA!: %s" % srcnodatavalue)

        # query DB
        codes = self.db_spatial.query(query)

        if codes:
            for r in codes:
                code = str(r[column_filter_code_index])
                label = str(r[column_filter_label_index])
                # TODO: handle the ST_Transform somehow
                query_extent = "SELECT ST_AsGeoJSON(ST_Extent(geom)) FROM " + from_query + " WHERE " + column_filter + " IN (" + code + ")"
                query_layer = "SELECT * FROM " + from_query + " WHERE " + column_filter + " IN (" + code + ")"
                filepath = crop_by_vector_database(raster_path, self.db_spatial, query_extent, query_layer)
                if filepath:
                    raster_stats = get_statistics(filepath, raster_statistics)
                    if raster_stats:
                        obj = {"code": code, "label": label, "data": raster_stats}
                        stats.append(obj)
        return stats

    def get_location_values(self, input_layers, lat, lon, band=None):
        input_files = []
        for input_layer in input_layers:
            input_files.append(self.get_raster_path(input_layer))
        log.info(input_files)
        return get_location_values(input_files, lat, lon, band)


# get the default db from the settings
def get_default_db(settings, dtype, connect=True):
    print "here"
    try:
        if "db" in settings:
            print settings
            db = settings["db"][dtype]
            if connect:
                print "here"
                return DBMSPostgreSQL(db)
            else:
                return db
        return None
    except:
        log.warn("No db found")
        pass