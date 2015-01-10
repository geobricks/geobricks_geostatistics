import logging

config = {

    "settings": {

        # Database
        "db": {
            # Spatial Database
            "spatial": {
                # default_db will search in the dbs["database"] as default option
                "dbname": "fenix",
                "host": "localhost",
                "port": "5432",
                "username": "user",
                "password": "pwd",
                "schema": "public"
            }
        }
    }
}
