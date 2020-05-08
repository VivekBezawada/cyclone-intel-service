# import sys
# from psycopg2.extras import execute_values
# import psycopg2 as pyc
# import json
# import os

# db_config = json.load(open(os.path.abspath("config.json"), "r"))


# # TODO : Add readme file to explain on conflict
# # SQL Insert queries
# INSERT_CYCLONE_INFO = "INSERT INTO cyclone_info (cyclone_id, cyclone_name, region) VALUES %s ON CONFLICT DO NOTHING"
# INSERT_TRACK_DATA = "INSERT INTO track_data (cyclone_id, synoptic_time, latitude, longitude, intensity) VALUES %s ON CONFLICT DO NOTHING"
# INSERT_FORECAST_DATA = "INSERT INTO forecast_data (cyclone_id, forecast_time, latitude, longitude, intensity) VALUES %s ON CONFLICT DO NOTHING"


# class DB:
#     def __init__(self):
#         try:
#             conn = pyc.connect(host=db_config["db_host"], port=db_config["db_port"],
#                         user=db_config["user"], password=db_config["password"], database=db_config["database"])
#             self.cur = conn.cursor()
#         except Exception as e:
#             print("Exception occured in conenecting database " + str(e))

#     def insert_data_into_tables(self, tuples):
#         execute_values(self.cur, INSERT_CYCLONE_INFO, tuples["cyclone_info"])
#         execute_values(self.cur, INSERT_TRACK_DATA, tuples["track_data"])
#         execute_values(self.cur, INSERT_FORECAST_DATA, tuples["forecast_data"])
#         self.conn.commit()
#         self.conn.close()
#         return

#     def update_data_into_tables(self, tuple):
#         #self.cur.execute()
#         # TODO : Write a update SQL query to change the status to false excluding these tuples
#         pass
