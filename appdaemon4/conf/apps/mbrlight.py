import appdaemon.plugins.hass.hassapi as hass
import datetime


class mbrlight(hass.Hass):
    def initialize(self):
        # self.listen_state(self.inputhandler, "light.mbr_plafond_level", old="off", new="on")
        self.listen_state(self.inputhandler, "light.mbr_plafond_level", old="off", new="on")
        self.listen_state(self.inputhandler2, "counter.douches", old="1", new="2")

        dimtime = datetime.time(1, 0, 0)
        brighttime = datetime.time(8, 0, 0)
        self.run_daily(self.changesetting, dimtime,value=4)
        self.run_daily(self.changesetting, brighttime,value=99)



        fetch_sunriseset_time = datetime.time(2, 0, 0)
        self.run_daily(self.fetch_sunriseset, fetch_sunriseset_time)
        self.fetch_sunriseset(1)
    
    def changesetting(self, value):
        #self.log("setting parameter")
        # self.call_service("zwave/set_config_parameter", node_id=kwargs["node_id"],parameter=kwargs["parameter"],value=kwargs["value"])
        value = value['value']
        topic = "OpenZWave/1/command/setvalue/"
        payload = '{ "ValueIDKey": 5348024802607121, "Value":'+str(value)+'}'
        self.call_service("mqtt/publish", topic=topic, payload=payload)

    def fetch_sunriseset(self, kwargs):


        self.sunrise_custom = self.sunrise().strftime("%H:%M:%S")
        self.sunset_custom = self.sunset().strftime("%H:%M:%S")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()
        counterdouches = float(self.get_state("counter.douches"))
        self.log(counterdouches)

        if self.now_is_between(self.sunrise_custom, self.sunset_custom):
            sundown = False
            sunup = True
        else:
            sundown = True
            sunup = False

        if self.now_is_between("11:00:00", "22:00:00"):
        # if 11 < now.hour <= 22:
            self.turn_on("light.mbr_plafond_level", brightness=254, transition=1)
            self.run_in(self.changesetting, 1,value=99)
            self.log("MBR max tussen 11 en 22")
        elif self.now_is_between("7:00:00", "22:00:00") and counterdouches >= 2:
            self.turn_on("light.mbr_plafond_level", brightness=254, transition=1)
            self.run_in(self.changesetting, 1,value=99)
            self.log("MBR max counterdouches = 2")
        elif self.now_is_between("7:00:00", "22:00:00") and sunup:
            self.turn_on("light.mbr_plafond_level", brightness=254, transition=1)
            # self.run_in(self.changesetting, 1,node_id=14,parameter=19,value=99)
            self.run_in(self.changesetting, 1, value=99)

            self.log("MBR max sunup")
        else:
            self.turn_on("light.mbr_plafond_level", brightness=10, transition=1)
            self.run_in(self.changesetting, 1, value=4)
            self.log("MBR dim")

        # if level == max:
        #     self.turn_on("light.mbr_plafond_level", brightness=254)
        # else:
        #     self.turn_on("light.mbr_plafond_level", brightness=10)


    def inputhandler2(self, entity, attribute, old, new, kwargs):
        # now = datetime.datetime.now()

        mbr_light = self.get_state("light.mbr_plafond_level")

        if self.now_is_between("7:00:00", "12:00:00") and mbr_light == "on":
            self.turn_on("light.mbr_plafond_level", brightness=254, transition=1)
            self.changesetting(value=99)
            self.log("MBR max terwijl licht al aan is. douchesv= 2")
