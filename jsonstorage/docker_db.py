
import os

dbs = {
    "psql":"django.db.backends.postgresql",
    "mysql":"django.db.backends.mysql",
    "oracle":"django.db.backends.oracle",
    "sqlite":"django.db.backends.sqlite3",
    
    "postgis":"django.contrib.gis.db.backends.postgis",
    "spatialite":"django.contrib.gis.db.backends.spatialite",
    
    "psql_multitenant":"tenant_schemas.postgresql_backend",
}

def db_from_env(default_conf):
    
    ret = default_conf
    
    DB_ENGINE = os.getenv("DB_ENGINE")
    DB_ENGINE = dbs.get(DB_ENGINE, DB_ENGINE)
    DB_NAME   = os.getenv("DB_NAME")
    DB_PASS   = os.getenv("DB_PASS")
    DB_USER   = os.getenv("DB_USER")
    DB_HOST   = os.getenv("DB_HOST")
    DB_PORT   = os.getenv("DB_PORT")
    DB_EXTRAS = os.getenv("DB_EXTRAS")

    print(DB_ENGINE, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)

    if DB_ENGINE != "":
        ret = {
            "ENGINE":DB_ENGINE
        }
        if DB_NAME:
            ret["NAME"] = DB_NAME
        if DB_USER:
            ret["USER"] = DB_USER
        if DB_PASS:
            ret["PASSWORD"] = DB_PASS
        if DB_HOST:
            ret["HOST"] = DB_HOST
        if DB_PORT:
            ret["PORT"] = DB_PORT
        
        
    return ret