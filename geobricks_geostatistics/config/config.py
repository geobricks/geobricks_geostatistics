import logging

config = {

    "settings": {

        # Database
        "db": {
            # Spatial Database
            "spatial": {
                # default_db will search in the dbs["database"] as default option
                "dbname": "db",
                "host": "localhost",
                "port": "5432",
                "username": "fenix",
                "password": "psw",
                "schema": "public"
            }
        }
    }
}
