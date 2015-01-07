import os
import json
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import get_raster_path, get_raster_path_published_by_uid
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
from geobricks_gis_raster.core.raster import crop_by_vector_database, get_statistics, get_srid, get_histogram, get_nodata_value, get_location_values

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
        '''
        :param json_stats: json with statistics definitions
        :return: json with response
        '''
        # Raster
        for raster in json_stats["raster"]:
            raster["path"] = get_raster_path(raster)

        # Vector
        # TODO: make an ENUM somewhere (i.e. database, geojson, etc)
        if json_stats["vector"]["type"] == "database":
            return self._zonal_stats_by_vector_database(json_stats)
        elif json_stats["vector"]["type"] == "geojson":
            log.warn("TODO: Geojson statistics not implemented yet")

        # Stats
        # TODO: save stats in case is needed or return statistics
        return None

    def get_stats(self, json_stats):
        return get_statistics(get_raster_path(json_stats["raster"]))

    def get_histogram(self, json_stats):
        return get_statistics(get_raster_path(json_stats["raster"]), json_stats["stats"])

    def _zonal_stats_by_vector_database(self, json_stats):
        # Stats result
        all_stats = []

        # raster statistics
        raster_statistics = None if "raster_stats" not in json_stats["stats"] else json_stats["stats"]["raster_stats"]

        # for each raster
        for raster in json_stats["raster"]:
            stats = []

            # get raster path
            raster_path = raster["path"]

            if raster_path is None:
                log.warn("Raster path is null for", raster)
            else:
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

                #srcnodatavalue = get_nodata_value(raster_path)
                # log.info("SRC NODATA!: %s" % srcnodatavalue)

                srid = get_srid(raster_path)
                print srid

                # query DB
                codes = self.db_spatial.query(query)

                if codes:
                    for r in codes:
                        code = str(r[column_filter_code_index])
                        label = str(r[column_filter_label_index])
                        # TODO: handle the ST_Transform somehow (i.e. transform the bounding box if srid is different?)
                        query_srid = "SELECT ST_SRID(geom) FROM gaul1_2015_4326 LIMIT 1;"
                        query_extent = "SELECT ST_AsGeoJSON(ST_Extent(ST_Transform(geom, " + srid + "))) FROM " + from_query + " WHERE " + column_filter + " IN (" + code + ")"
                        query_layer = "SELECT * FROM " + from_query + " WHERE " + column_filter + " IN (" + code + ")"
                        filepath = crop_by_vector_database(raster_path, self.db_spatial, query_extent, query_layer)
                        if filepath:
                            raster_stats = get_statistics(filepath, raster_statistics)
                            if raster_stats:
                                obj = {"code": code, "label": label, "data": raster_stats}
                                stats.append(obj)

            # add to all stats
            all_stats.append(stats)
        return all_stats

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