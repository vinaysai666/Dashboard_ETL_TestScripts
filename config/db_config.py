import sys

sys.dont_write_bytecode = True

DB_CONFIGS = {
    "source": {
        "type": "postgresql",
        "host": "prod-db-businessdashboard.cdlpzfk7lmni.ap-south-1.rds.amazonaws.com",
        "user": "reader",
        "password": "NIhicEu1I8FYUR5q",
        "database": "prodbd",
        "port":5432
    }
}


# DB_CONFIGS={
#     "source": {
#         "type": "postgresql",
#         "host": "13.202.155.21",
#         "user": "postgres",
#         "password": "Nst-bd-sit@2025",
#         "database": "sitdashboard",
#         "port":5434
#     }
# }