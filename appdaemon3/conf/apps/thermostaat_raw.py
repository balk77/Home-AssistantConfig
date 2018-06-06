import appdaemon.plugins.hass.hassapi as hass

class thermostaat_raw(hass.Hass):
    def initialize(self):

        self.listen_state(self.inputhandler, "sensor.thermostaat_tempsetpoint_raw")


    def inputhandler(self, entity, attribute, old, new, kwargs):
        reading = self.get_state("sensor.thermostaat_tempsetpoint_raw")
        #self.log(reading)
        if reading != "undefined":
            try:
                temp_sp_thermostaat = float(reading)
                #self.log("float: " + reading )
                self.set_state("sensor.thermostaat_tempsetpoint", state=temp_sp_thermostaat)
            except:
                self.log("error in: reading" + reading)

