import appdaemon.plugins.hass.hassapi as hass

class thermostaat_raw(hass.Hass):
    def initialize(self):

        self.listen_state(self.inputhandler, "sensor.thermostaat_tempsetpoint_raw")


    def inputhandler(self, entity, attribute, old, new, kwargs):

        if self.get_state("sensor.thermostaat_tempsetpoint_raw") != "undefined":
            temp_sp_thermostaat = float(self.get_state("sensor.thermostaat_tempsetpoint_raw"))

            self.set_state("sensor.thermostaat_tempsetpoint", state=temp_sp_thermostaat)
