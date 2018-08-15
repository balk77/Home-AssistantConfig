import appdaemon.plugins.hass.hassapi as hass
import datetime


class mbrlight(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, "light.mbr_plafond_level", old="off", new="on")
        self.listen_state(self.inputhandler2, "counter.douches", old="1", new="2")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()

        if now.hour >= 22 or (self.sun_down() or now.hour < 7 and now.hour < 11):
            self.turn_on("light.mbr_plafond_level", brightness=26)
            self.log("MBR dim")
        else:
            self.turn_on("light.mbr_plafond_level", brightness=254)
            self.log("MBR max")

    def inputhandler2(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()

        mbr_light = self.get_state("light.mbr_plafond_level")

        if now.hour < 12 and mbr_light == "on":
            self.turn_on("light.mbr_plafond_level", brightness=254)
            self.log("MBR max")
