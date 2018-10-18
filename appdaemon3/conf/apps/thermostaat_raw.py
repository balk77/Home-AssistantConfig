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
                self.log("float: " + reading )
                
                #self.call_service("input_number/set_value", entity_id="input_number.thermostaat_setpoint", value=temp_sp_thermostaat)
                self.call_service("mqtt/publish", topic="woonkamer/woonkamer/thermostaat/tempsetpoint2", payload=temp_sp_thermostaat, retain=True)
                

                #self.set_state("sensor.thermostaat_tempsetpoint", state=temp_sp_thermostaat)
            except:
                self.log("error in: reading" + reading)

