import appdaemon.plugins.hass.hassapi as hass
import datetime


class mbrlight(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, "light.mbr_plafond_level", old="off", new="on")
        self.listen_state(self.inputhandler2, "counter.douches", old="1", new="2")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()
        counterdouches = float(self.get_state("counter.douches"))
        self.log(counterdouches)

        if 11 < now.hour <= 22:
            self.turn_on("light.mbr_plafond_level", brightness=254)
            self.log("MBR max tussen 11 en 22")
        elif now.hour < 22 and counterdouches >= 2:
            self.turn_on("light.mbr_plafond_level", brightness=254)
            self.log("MBR max counterdouches = 2")
        elif 7 <= now.hour < 22 and self.sun_up():
            self.turn_on("light.mbr_plafond_level", brightness=254)

            self.log("MBR max sunup")
        else:
            self.turn_on("light.mbr_plafond_level", brightness=10)
            self.log("MBR dim")

        # if level == max:
        #     self.turn_on("light.mbr_plafond_level", brightness=254)
        # else:
        #     self.turn_on("light.mbr_plafond_level", brightness=10)


    def inputhandler2(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()

        mbr_light = self.get_state("light.mbr_plafond_level")

        if now.hour < 12 and mbr_light == "on":
            self.turn_on("light.mbr_plafond_level", brightness=254)
            self.log("MBR max terwijl licht al aan is. douchesv= 2")
