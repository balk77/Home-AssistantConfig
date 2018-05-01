import appdaemon.plugins.hass.hassapi as hass
import datetime


class mbrlight(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, "light.mbr_plafond_level", old="off", new="on")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()

        if now.hour >= 22 or (self.sun_down() and now.hour < 11):
            self.turn_on("light.mbr_plafond_level", brightness=26)
            self.log("MBR dim")
        else:
            self.turn_on("light.mbr_plafond_level", brightness=254)
            self.log("MBR max")
