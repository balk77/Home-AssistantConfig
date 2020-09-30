import appdaemon.plugins.hass.hassapi as hass
import datetime
import random
import json
import psycopg2
# from config import config




class showergasuse(hass.Hass):
    def initialize(self):
        
        
        self.listen_state(self.inputhandler, "input_boolean.test",new="onnnnn")
        

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()

        d = {}
        

        # self.log(datetime.timezone)
        timestamp = datetime.datetime(now.year,now.month,now.day,now.hour-2)
        value = random.random()

        # d["timestamp"] = timestamp
        d["year"]= now.year
        d["month"]= now.month
        d["day"]= now.day
        d["hour"]= now.hour-2
        
        d["hourlyshowergasusage"] = value
        # payload = '{"timestamp": timestamp,"hourlyshowergasusage":}'
        payload = json.dumps(d, ensure_ascii=False)

        self.call_service("mqtt/publish", topic="zolder/hourlyshowergasusage", payload=payload, retain=True)
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.test")

        conn = None
        # try:
        #     # params = config()
        #     # conn = psycopg2.connect(**params)
        #     conn = psycopg2.connect(user = "postgres",
        #                           password = "RMzK5tzHN2zebj",
        #                           host = "192.168.0.9",
        #                           port = "5432",
        #                           database = "dsmrreader")
        #     cur = conn.cursor()
        #     cur.execute("SELECT * FROM public.dsmr_stats_hourstatistics ORDER BY id DESC LIMIT 1")
        #     self.log("The number of parts: ", cur.rowcount)
        #     row = cur.fetchone()
    
        #     while row is not None:
        #         self.log(row)
        #         row = cur.fetchone()
    
        #     cur.close()
        # except (Exception, psycopg2.DatabaseError) as error:
        #     self.log(error)
        #     self.log("x")
        # finally:
        #     if conn is not None:
        #         conn.close()
        

        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(user = "postgres",
                                password = "RMzK5tzHN2zebj",
                                host = "192.168.0.9",
                                port = "5432",
                                database = "dsmrreader")
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.dsmr_stats_hourstatistics ORDER BY id DESC LIMIT 1")
        self.log(cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            self.log(row)
            row = cur.fetchone()

        cur.close()
    
        conn.close()

