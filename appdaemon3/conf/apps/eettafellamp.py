import appdaemon.plugins.hass.hassapi as hass
import datetime


class eettafellamp(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, "light.wk_eettafel_plafond_level", old = "off", new = "on")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()

        if now.hour >= 20 or now.hour < 3:
            self.turn_on("light.wk_eettafel_plafond_level")
        else:
            self.turn_on("light.wk_eettafel_plafond_level", brightness=255)

